 
const wirings = {
                    //[Turn toward light, Faster closer to light]
    aggression:     s =>[1, 1],
    love:           s => [1, -1],
    fear:           s => [-1, 1], 
    explorer:       s => [-1, -1]
}

const speed_scalar = 25
const dir_scalar = 1/30

class vehicle {
    constructor(initial_coords, initial_dir, options){
        
        // Ensures at least SOMETHING was input for options 
        if (options == undefined){
            options = {}; 
        }
        
        this.coords = initial_coords; // Initializes vehicle position - is an array of length 2
        this.dir_rad = initial_dir; // Vehicle direction in radians
        this.dir_cart = [Math.cos(this.dir_rad), Math.sin(this.dir_rad)]; // Initial vehicle direction - array of length two that is unit vector


        
        // Makes sure the option inputed is among the four defined options. If not, default to aggression
        if (options.wiring !== undefined){
            this.wiring = wirings[options.wiring]();
        } else{
            this.wiring = wirings.aggression();
        }

        for (let key in options){
            if (key !== "wiring"){
                this[key] = options[key];
            }
        }


    }

    // Calculates distance between a vehicle and light source given coordinates
    distance(v, light){
        return Math.sqrt(Math.pow(light[0]-v[0], 2) + Math.pow(light[1]-v[1], 2));
    }

    // Calculates the magnitude of a vector
    magnitude(vector){
        return Math.sqrt(Math.pow(vector[0], 2) + Math.pow(vector[1], 2));
    }  

    // Calculates dot product between two vectors
    dot_product(v1, v2){
        return (v1[0]*v2[0]) + (v1[1]*v2[1]);
    }

    // Normalizes input vector
    normalize(v){
        let mag = this.magnitude(v);
        return [v[0]/mag, v[1]/mag];
    }


    // Calculates smaller angle between vehicle direction vector and light source distance vector (dot product)
    theta_diff(dir, dist){
        // Clamped to [-1, 1] so floating point error can't push acos into NaN
        let cos_theta = this.dot_product(dir, dist)/(this.magnitude(dir) * this.magnitude(dist));
        return Math.acos(Math.max(-1, Math.min(1, cos_theta)));
    }

    // Calculates the direction the vehicle should turn to get closer (1 for counterclockwise, -1 for clockwise)
    turn_dir(dir, light){
        let d = dir[0]*light[1] - dir[1]*light[0];
        // d is 0 when aligned or directly opposite, so avoid dividing by it
        return d >= 0 ? 1 : -1;
    }

    // Update the position of the vehicle by averaging the weighted distance to all light sources (all other vehicles)
    update(sources){
        // Nothing else to be drawn toward
        if (sources.length < 2){
            return;
        }

        let totx = 0
        let toty = 0
        for (let i = 0; i<sources.length; i++){
            if (sources[i] !== this){
                // Vector toward the source, scaled by 1/d^3 so its magnitude falls off as 1/d^2
                let d = this.distance(this.coords, sources[i].coords);
                totx += (sources[i].coords[0] - this.coords[0])/Math.pow(d, 3);
                toty += (sources[i].coords[1] - this.coords[1])/Math.pow(d, 3);
            }
        }

        // light_dir = [lightx, lighty] is the direction the vehicle should be oriented for the most light
        let lightx = totx/(sources.length-1);
        let lighty = toty/(sources.length-1);
        
        let light_dir = [lightx, lighty];

        // Actual assigned change in direction 
        let theta_change = dir_scalar*this.theta_diff(this.dir_cart, light_dir);

        let counterclockwise = this.turn_dir(this.dir_cart, light_dir);

        // Update direction in radians
        this.dir_rad += this.wiring[0]*counterclockwise*theta_change;

        // Update cartesian direction
        this.dir_cart = [Math.cos(this.dir_rad), Math.sin(this.dir_rad)];

        // Wiring of 1 speeds up with the magnitude of light_dir, -1 slows down with it
        let intensity = this.magnitude(light_dir);
        let speed = this.wiring[1] === 1 ? speed_scalar*intensity : speed_scalar/(1 + intensity);

        let changex = speed*this.dir_cart[0];
        let changey = speed*this.dir_cart[1];

        this.coords[0] += changex;
        this.coords[1] += changey;
    }

}