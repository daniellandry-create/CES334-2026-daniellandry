let socket;

const NUM_DAY_IMAGES = 3;
const NUM_NIGHT_IMAGES = 3;
const FADE_DURATION = 2000; // milliseconds

let current_image = null;
let next_image = null;
let fade_start = 0;

// AI-assisted
function drawImageCover(img) {
    const scale = Math.max(width / img.width, height / img.height);

    const w = img.width * scale;
    const h = img.height * scale;

    image(img, (width - w) / 2, (height - h) / 2, w, h);
}

// AI-assisted
function transition_day(new_state) {
    console.log(`Received new state: ${new_state}`);

    if (new_state !== "day" && new_state !== "night") return;

    const count = new_state === "day" ? NUM_DAY_IMAGES : NUM_NIGHT_IMAGES;
    const index = Math.floor(Math.random() * count) + 1;

    loadImage(`assets/${new_state}${index}.jpg`, (img) => {
        // Finish any previous transition
        if (next_image) current_image = next_image;

        next_image = img;
        fade_start = millis();
    });
}

// Human programmed
function setup() {
    // Canvas setup
    createCanvas(windowWidth, windowHeight);
    frameRate(60);

    // WebSocket setup
    socket = new WebSocket("ws://127.0.0.1:8767");

    socket.onopen = () => {
        console.log("Connected to websocket server");

        socket.send(JSON.stringify({
            request: "get_state"
        }));
    };

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        transition_day(data.new_state);
    };

    socket.onerror = (error) => {
        console.error("WebSocket error:", error);
    };

    socket.onclose = () => {
        console.log("WebSocket closed:", event);
    };
}

// AI-assisted
function draw() {
    background(0);

    if (current_image) {
        drawImageCover(current_image);
    }

    if (next_image) {
        let alpha = constrain((millis() - fade_start) / FADE_DURATION, 0, 1);

        tint(255, alpha * 255);
        drawImageCover(next_image);
        noTint();

        if (alpha >= 1) {
            current_image = next_image;
            next_image = null;
        }
    }
}

function windowResized() {
    resizeCanvas(windowWidth, windowHeight);
}