 
const wirings = {
                    //[Speeds up closer to light, turns toward light]
    fear:           s => [1/s.dist, s.dot*s.omega], 
    aggression:     s =>[1/s.dist, -s.dot*s.omega],
    love:           s => [1- (1/s.dist), s.dot*s.omega],
    explorer:       s => [1 - (1/s.dist), -s.dot*s.omega]
}

class vehicle {
    constructor(startX, startY, options){
        
        //ensures at least SOMETHING was input for options 
        if (options == undefined){
            options = {}; 
        }

        //initializes vehicle position
        this.x = startX;
        this.y = startY;
        
        //makes sure the option inputed is among the four defined options. If not, default to aggression
        if (options.wiring !== undefined){
            this.wiring = options.wiring;
        } else{
            this.wiring = wirings/aggression
        }

        for (let key in options){
            if (key != wiring){
                this[key] = options[key];
            }
        }

    }

    update(){
        
    }
}