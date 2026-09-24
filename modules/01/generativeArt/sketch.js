// Where your "setup()" and "draw()" functions live
const sources = [];
let screen_size;
let num_vehicles;
let vehicle_size;
const options = ['aggression', 'love', 'fear', 'explorer'];
const colors = ['#08f14f', '#7c1ddc', '#0a5eef','#1adec6'];


function setup(){
    createCanvas(windowWidth, windowHeight);
    console.log("windowWidth:", windowWidth, "windowHeight", windowWidth);
    screen_size = (windowWidth*windowHeight);
    num_vehicles = Math.floor(screen_size/500000) + 4;
    vehicle_size = Math.floor(screen_size/180000) + 5;
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