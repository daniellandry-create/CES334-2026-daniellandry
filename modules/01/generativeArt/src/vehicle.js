 
const wirings = {
                    //[Speeds up closer to light, turns toward light]
    fear:           s => [1/s.dist, s.dot*s.omega], 
    aggression:     s =>[1/s.dist, -s.dot*s.omega],
    love:           s => [1- (1/s.dist), s.dot*s.omega],
    explorer:       s => [1 - (1/s.dist), -s.dot*s.omega]
}

const speed_scalar = 5

class vehicle {
    constructor(initial_coords, initial_dir, options){
        
        //ensures at least SOMETHING was input for options 
        if (options == undefined){
            options = {}; 
        }
        
        this.coords = initial_coords //initializes vehicle position - is an array of length 2
        this.dir = initial_dir //initial vehicle direction - array of length two that is unit vector
        
        //makes sure the option inputed is among the four defined options. If not, default to aggression
        if (options.wiring !== undefined){
            this.wiring = options.wiring;
        } else{
            this.wiring = wirings.aggression;
        }

        for (let key in options){
            if (key != wiring){
                this[key] = options[key];
            }
        }


    }

    //calculates distance between a vehicle and light source given coordinates
    distance(v, light){
        return Math.sqrt(Math.pow(light[0]-v[0], 2) + Math.pow(light[1]-v[1], 2));
    }

    //calculates the magnitude of a vector
    magnitude(vector){
        return Math.sqrt(Math.pow(vector[0], 2) + Math.pow(vector[1], 2));
    }  

    //calculates dot product between two vectors
    dot_product(v1, v2){
        return (v1[0]*v2[0]) + (v1[1]*v2[1]);
    }


    //calculates smaller angle between vehicle direction vector and light source distance vector (dot product)
    // theta_diff(dir, dist){
    //     return Math.acos(this.dot_product(dir, dist)/(this.magnitude(dir) * this.magnitude(dist)));
    // }

    //calculates the direction the vehicle should turn to get closer (1 for counterclockwise, -1 for clockwise)
    turn_dir(dir, light){
        let x = dir[0]*light[1] - dir[1]*light[0]; 
        if (x>0) return 1;
        return -1;
    }

    //update the position of the vehicle by averaging distance to all light sources (all other vehicles)
    update(sources){
        let tot_dist = 0
        for (let i = 0; i<sources.length; i++){
            tot_dist += this.distance(sources[i], this.coords);
        }
        
        let avg_dist = tot_dist/(sources.length - 1);
        let new_speed = speed_scalar*(1/Math.pow(avg_dist, 2));
        let new_dir = turn_dir(this.dir, souces[i])
    }

    dist
}