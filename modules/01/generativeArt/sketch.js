// Where your "setup()" and "draw()" functions live
const sources = [];
const num_vehicles = 25;
const options = ['aggression', 'love', 'fear', 'explorer'];
const colors = ['red', 'purple', 'blue','orange'];
const vehicle_size = 100


function setup(){
    createCanvas(windowWidth, windowHeight);
    for (let i = 0; i<num_vehicles; i++){
        num = Math.floor(4 * Math.random());
        sources[i] = new vehicle([random(width), random(height)], random(TWO_PI), {wiring: options[num]}, colors[num]);
    }

}

function draw(){
    background(0, 10);
    noStroke();
    let bad = 0;
    for (let i = 0; i < sources.length; i++){
        if (!isFinite(sources[i].coords[0]) || !isFinite(sources[i].coords[1])) bad++;
        fill(sources[i].clr);
        circle(sources[i].coords[0], sources[i].coords[1], vehicle_size);
        sources[i].update(sources);
    }
    if (bad > 0) console.log(bad, "/", sources.length, "vehicles non-finite at frame", frameCount);

}