// Where your "setup()" and "draw()" functions live
const sources = [];
const num_vehicles = 5;
const options = ['aggression', 'love', 'fear', 'explorer'];
const colors = ['red', 'orange', 'yellow'];
let color;

function setup(){
    createCanvas(windowWidth, windowHeight);
    for (let i = 0; i<num_vehicles; i++){
        num = Math.floor(4 * Math.random());
        sources[i] = vehicle(options[num]);
    }

}

function draw(){
    background(220);
    nostroke();
    color = Math.floor(3*Math.random());
    fill('blue');
    for (let i = 0; i < sources.length; i++){
        circle(sources[i].coords[0]%windowWidth, sources[i].coords[1]%windowHeight);
        sources[i].update(sources);
    }
}