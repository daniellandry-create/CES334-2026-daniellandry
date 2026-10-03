#ifndef PLAYER_H
#define PLAYER_H

#include <string>
using namespace std;

class Player {
public:
    Player(int x, int y,);
    struct coords{
        double x;
        double y;
    };
    
    string type;
};

#endif