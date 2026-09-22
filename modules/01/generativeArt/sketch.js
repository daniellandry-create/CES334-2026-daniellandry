// Where your "setup()" and "draw()" functions live
const sources = [];
const num_vehicles = 500;
const options = ['aggression', 'love', 'fear', 'explorer'];
const colors = ['red', 'purple', 'blue','orange'];
const vehicle_size = 15


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
    for (let i = 0; i < sources.length; i++){
        fill(sources[i].clr);
        circle(sources[i].coords[0], sources[i].coords[1], vehicle_size);
        sources[i].update(sources);
    }
}