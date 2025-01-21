const canvas = document.getElementById('dartboard');

if (window.innerHeight < window.innerWidth) {
    var calculatedSize = window.innerHeight - 200
    var layout = "horizontal"
} else {
    var calculatedSize = window.innerWidth - 200
    var layout = "vertical"
}

canvas.width = calculatedSize
canvas.height = calculatedSize

const ctx = canvas.getContext('2d');
const centerX = canvas.width / 2;
if (layout === "vertical") {
    var centerY = canvas.height / 2;
} else {
    var centerY = canvas.height / 2;
}

const radius = canvas.width / 2 - 30; // Inset to leave space for numbers
const segmentCount = 20; // Number of segments
const numbers = [20, 1, 18, 4, 13, 6, 10, 15, 2, 17, 3, 19, 7, 16, 8, 11, 14, 9, 12, 5];
const colorPalette = ["rgb(15, 15, 15, 0.8)", "rgb(156, 156, 156, 0.5)", "rgb(15, 15, 15, 0.8)", "rgb(156, 156, 156, 0.5)", "rgb(15, 15, 15, 0.8)", "rgb(156, 156, 156, 0.5)", "rgb(15, 15, 15, 0.8)", "rgb(156, 156, 156, 0.5)", "rgb(15, 15, 15, 0.8)", "rgb(156, 156, 156, 0.5)", "rgb(15, 15, 15, 0.8)", "rgb(156, 156, 156, 0.5)", "rgb(15, 15, 15, 0.8)", "rgb(156, 156, 156, 0.5)", "rgb(15, 15, 15, 0.8)", "rgb(156, 156, 156, 0.5)", "rgb(15, 15, 15, 0.8)", "rgb(156, 156, 156, 0.5)", "rgb(15, 15, 15, 0.8)", "rgb(156, 156, 156, 0.5)"]; // Red and Green for normal segments

// Segment object definition
class Segment {
    constructor(index, number) {
        this.index = index;
        this.number = number;
        this.angle = (index * (2 * Math.PI)) / segmentCount - Math.PI / 2; // Angle for the segment
        this.highlighted = false; // State to track if the segment is highlighted
        this.startAngle = this.angle;
        this.endAngle = this.angle + (2 * Math.PI) / segmentCount;
        this.color = colorPalette[index % colorPalette.length]; // Alternate between red and green
    }

    // Method to draw the segment
    drawSegment() {
        // Draw the segment itself
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius, this.startAngle, this.endAngle);
        ctx.lineTo(centerX, centerY);
        ctx.closePath();

        // Color based on type (single, double, triple)
        ctx.fillStyle = this.color;
        ctx.fill();
    }

    highlightSegment() {
        // Draw the segment itself
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius, this.startAngle, this.endAngle);
        ctx.lineTo(centerX, centerY);
        ctx.closePath();

        // Color based on type (single, double, triple)
        ctx.fillStyle = "#0f04e0";
        ctx.fill();
    }

    drawNumber() {
        // Draw the number
        const numberX = centerX + Math.cos(this.angle + Math.PI / segmentCount) * (radius + 15);
        const numberY = centerY + Math.sin(this.angle + Math.PI / segmentCount) * (radius + 15);
        ctx.font = "20px Helvetica";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillStyle = "white";
        ctx.fillText(this.number, numberX, numberY);
    }

    drawDoubleRing() {
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius * 1, this.startAngle, this.endAngle); // Radius for double ring
        ctx.lineWidth = 1;
        ctx.strokeStyle = "#FFD700"; // Golden color for Double
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(centerX, centerY, radius * 0.95, this.startAngle, this.endAngle); // Radius for double ring
        ctx.lineWidth = 1;
        ctx.strokeStyle = "#FFD700"; // Golden color for Double
        ctx.stroke();
    }

    highlightDoubleRing() {
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius * 1, this.startAngle, this.endAngle); // Radius for double ring
        ctx.lineWidth = 5;
        ctx.strokeStyle = "#0f04e0"; // Golden color for Double
        ctx.stroke();
    }

    drawTripleRing() {
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius * 0.65, this.startAngle, this.endAngle); // Radius for triple ring
        ctx.lineWidth = 1;
        ctx.strokeStyle = "#FFD700"; // Golden color for Triple
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(centerX, centerY, radius * 0.60, this.startAngle, this.endAngle); // Radius for triple ring
        ctx.lineWidth = 1;
        ctx.strokeStyle = "#FFD700"; // Golden color for Triple
        ctx.stroke();
    }

    highlightTripleRing() {
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius * 0.65, this.startAngle, this.endAngle); // Radius for triple ring
        ctx.lineWidth = 5;
        ctx.strokeStyle = "#0f04e0"; // Golden color for Triple
        ctx.stroke();
    }
}

// Create the segments array
const segments = numbers.map((num, index) => new Segment(index, num));

// Draw the entire dartboard
function drawDartboard() {
    ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear canvas

    // Draw the outer circle for the dartboard
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
    ctx.strokeStyle = "#000"; // Black outline
    ctx.lineWidth = 3;
    ctx.stroke();
    ctx.lineWidth = 1; // Reset line width for other shapes

    // Apply rotation to the canvas
    ctx.save(); // Save the current context
    ctx.translate(centerX, centerY); // Move the origin to the center of the canvas
    ctx.rotate(-0.16); // Apply the rotation
    ctx.translate(-centerX, -centerY); // Move the origin back
    // Draw each segment
    segments.forEach(segment => segment.drawSegment());
    segments.forEach(segment => segment.drawDoubleRing());
    segments.forEach(segment => segment.drawTripleRing());
    segments.forEach(segment => segment.drawNumber());

    ctx.lineWidth = 1; // Reset line width for other shapes
}

function highlight_segment(segmentValue) {
    segments.forEach(segment => {
        if (segment.number === segmentValue) {
            segment.highlightSegment()
        }
    });
}

drawDartboard();
// setInterval(fetchHitData, 1000); // Poll every second