 
const wirings = {
                    //[Turn toward light, Faster closer to light]
    aggression:     s =>[1, 1],
    love:           s => [1, -1],
    fear:           s => [-1, 1], 
    explorer:       s => [-1, -1]
}

const speed_scalar = 5;
const min_speed = 0.5;
const pixels = 10;
const dir_scalar = 1/75

class vehicle {
    constructor(initial_coords, initial_dir, options, clr){
        
        // Ensures at least SOMETHING was input for options 
        if (options == undefined){
            options = {}; 
        }
        
        this.coords = initial_coords; // Initializes vehicle position - is an array of length 2
        this.dir_rad = initial_dir; // Vehicle direction in radians
        this.dir_cart = [Math.cos(this.dir_rad), Math.sin(this.dir_rad)]; // Initial vehicle direction - array of length two that is unit vector

        // Initialize color
        this.clr = clr;
        
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

    // Calculates the [x, y] offset from this vehicle to a light source.
    // Because the screen wraps around, a source can be reached two ways along each axis:
    // directly, or by going through the edge. We pick whichever way is shorter.
    wrapped_offset(v, light){
        let dx = light[0] - v[0];
        let dy = light[1] - v[1];

        // If the source is more than half the screen away, it's closer going through the edge
        if (dx > width/2){
            dx = dx - width;
        }
        if (dx < -width/2){
            dx = dx + width;
        }
        if (dy > height/2){
            dy = dy - height;
        }
        if (dy < -height/2){
            dy = dy + height;
        }

        return [dx, dy];
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
        let cos_theta = this.dot_product(dir, dist)/(this.magnitude(dir) * Math.max(this.magnitude(dist), 0.0001));
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
        let nearest = Infinity // Distance to the closest other vehicle (the brightest light)
        for (let i = 0; i<sources.length; i++){
            if (sources[i] !== this){
                // Offset toward the source, taking the shortest path (possibly through a screen edge)
                let offset = this.wrapped_offset(this.coords, sources[i].coords);
                let d = this.magnitude(offset);

                // Vector toward the source, divided by d^2 so closer sources pull harder
                totx += offset[0]/Math.pow(Math.max(d, 0.01), 2);
                toty += offset[1]/Math.pow(Math.max(d, 0.01), 2);

                // Keep track of the closest source
                if (d < nearest){
                    nearest = d;
                }
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

        // How close the nearest source is, from 0 (as far away as possible) to 1 (right on top of us).
        // With wrapping, the farthest anything can be is half the screen diagonal.
        let max_dist = Math.sqrt(Math.pow(width/2, 2) + Math.pow(height/2, 2));
        let closeness = 1 - nearest/max_dist;

        // Wiring of 1 goes faster when closer to light, -1 goes slower when closer to light
        let speed;
        if (this.wiring[1] === 1){
            speed = speed_scalar*closeness;
        } else {
            speed = speed_scalar*(1 - closeness);
        }

        // Small minimum so no vehicle gets completely stuck
        speed = Math.max(speed, min_speed);

        let changex = speed*this.dir_cart[0];
        let changey = speed*this.dir_cart[1];

        // Update coordinates
        this.coords[0] += changex;
        this.coords[1] += changey;

        // Wrap around to other side of screen if necessary
        this.coords[0] = ((this.coords[0] % width) + width) % width;
        this.coords[1] = ((this.coords[1] % height) + height) % height;

    }

}