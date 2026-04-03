from flask import Flask, request, jsonify, render_template
import random

app = Flask(__name__)

# Sample question data, organized by difficulty level
questions = {
    'easy': [
        {
            'id': 1,
            'text': 'The figure shows three paths connecting points a and b. A single force does the indicated work on a particle moving along each path in the indicated direction. On the basis of this information, is force  conservative?',
            'img': ['1.png'],
            'options': ['Yes', 'No'], 'answer': 'No', 'analysis': 'Ppt 9, section 8-1'
        },
        {
            'id': 2,
            'text': 'A particle is to move along an x axis from x = 0 to x1 while a conservative force, directed along the x axis, acts on the particle. The figure shows three situations in which the x component of that force varies with x. The force has the same maximum magnitude F1 in all three situations. Rank the situations according to the change in the associated potential energy during the particle’s motion, most positive first.',
            'img': ['2.png'],
            'options': ['1>2>3', '3>2>1', '1>3>2', '3>1>2'], 'answer': '3>1>2', 'analysis': 'Ppt 9, section 8-1'
        },
        {
            'id': 3,
            'text': 'The figure shows four situations—one in which an initially stationary block is dropped and three in which the block is allowed to slide down frictionless ramps. Rank the situations according to the kinetic energy of the block at point B, greatest first.',
            'img': ['3.png'],
            'options': ['4>3>2>1', '1>2>3>4', '1=2=3=4', '4=3=2>1'], 'answer': '1=2=3=4',
            'analysis': 'Ppt 9, section 8-2'
        },
        {
            'id': 4,
            'text': 'A particle is to be placed, in turn, outside four objects, each of mass m: (1) a large uniform solid sphere, (2) a large uniform spherical shell, (3) a small uniform solid sphere, and (4) a small uniform shell. In each situation, the distance between the particle and the center of the object is d. Rank the objects according to the magnitude of the gravitational force they exert on the particle, greatest first.',
            'options': ['1=2=3=4', '1=2>3=4', '1>2>3>4', '1>2=3>4'], 'answer': '1=2=3=4',
            'analysis': 'Ppt 11, section 13-1'
        },
        {
            'id': 5,
            'text': 'You move a ball of mass m away from a sphere of mass M. (a) Does the gravitational potential energy of the system of ball and sphere increase or decrease? (b) Is positive work or negative work done by the gravitational force between the ball and the sphere?',
            'options': ['increase; positive', 'increase; negative', 'decrease; positive', 'decrease; negative'],
            'answer': 'increase; negative', 'analysis': 'Ppt 11, section 13-5'
        },
        {
            'id': 6,
            'text': 'Satellite 1 is in a certain circular orbit around a planet, while satellite 2 is in a larger circular orbit. Which satellite has (a) the longer period and (b) the greater speed?',
            'options': ['1; 1', '1; 2', '2; 1', '2; 2'], 'answer': '2; 1', 'analysis': 'Ppt 11, section 13-6'
        }
        
    ],
    'medium': [
        {
            'id': 7,
            'text': 'The periods of a spring oscillator (under horizontal SHM) and a pendulum are T1 and T2, respectively. If they are placed in the moon with decreased gravitational acceleration, the periods become T1’ and T2’. Then',
            'options': ['T1’> T1 and T2’> T2', 'T1’< T1 and T2’< T2', 'T1’= T1 and T2’= T2', 'T1’= T1 and T2’> T2'],
            'answer': 'T1’= T1 and T2’> T2', 'analysis': 'Ppt 12'
        },
        {
            'id': 8,
            'text': 'A sinusoidal wave is traveling along the negative direction of x axis, with angular frequency of ω and traveling velocity of u. If the waveform at t=T/4 is as the figure below, then the wave can be expressed as:',
            'img': ['8.png'],
            'options': ['/static/imgs/8-1.png', '/static/imgs/8-2.png', '/static/imgs/8-3.png', '/static/imgs/8-4.png'],
            'answer': '/static/imgs/8-4.png', 'analysis': 'Ppt 12'
        },
        {
            'id': 9,
            'text': 'When an aerospace shuttle (mass m) returns to the Earth with engine off, in which the distance between itself to the Earth center changes from R1 to R2, the increased kinetic energy of the shuttle will be: (M as Earth mass, G as the gravitational constant)',
            'options': ['/static/imgs/9-1.png', '/static/imgs/9-5.png', '/static/imgs/9-3.png', '/static/imgs/9-4.png',
                        '/static/imgs/9-5.png'], 'answer': '/static/imgs/9-3.png', 'analysis': 'Ppt 11'
        },
        {
            'id': 10,
            'text': 'A spring with spring constant k was placed on an inclined surface with inclination angle α, in which one end was fixed on Baffle A, and the other end was connected to object B with mass m. Point O is the balance position with no connected object B, and point a is the equilibrium position with connection of object B. Now move object B from point a along the slope to point b (as shown in the picture). Assume that the distances between point a and point O, and point a and point b are x1 and x2, respectively, then during this process, the potential energy of the system composed of spring, object B and the earth increases as',
            'img': ['10.png'],
            'options': ['/static/imgs/10-1.png', '/static/imgs/10-2.png', '/static/imgs/10-3.png',
                        '/static/imgs/10-4.png'], 'answer': '/static/imgs/10-3.png', 'analysis': 'Ppt 9'
        },
        {
            'id': 11,
            'text': 'Two waves are with initial phases φ1 and φ2, starting from points S1 and S2, respectively. The wavelength is λ for both. To make an construction interference, we should have:',
            'img': ['11.png'],
            'options': ['/static/imgs/11-1.png', '/static/imgs/11-2.png', '/static/imgs/11-3.png',
                        '/static/imgs/11-4.png'], 'answer': '/static/imgs/11-3.png', 'analysis': 'Ppt 13'
        },
        {
            'id': 12,
            'text': 'A satellite moves around the Earth in an ellipse shape, with the largest and the smallest distance as RA and RB. What is the relationship between angular momentum and kinetic energy at these two points?',
            'img': ['12.png'],
            'options': ['LB > LA，EKA > EKB', 'LB > LA，EKA = EKB', 'LB = LA，EKA = EKB', 'LB < LA，EKA = EKB',
                        'LB = LA，EKA < EKB'],
            'answer': 'LB = LA，EKA < EKB', 'analysis': 'Ppt 11'
        },
        {
            'id': 13,
            'text': 'Several forces act simultaneously on a rigid body with a smooth fixed axis of rotation. If the vector sum of these forces is zero, then the rigid body: ',
            'options': ['will definitely not rotate', 'will definitely not change its angular velocity', 'will definitely change its angular velocity', 'may or may not change its angular velocity'],
            'answer': 'may or may not change its angular velocity', 'analysis': 'None'
        },
        {
            'id': 14,
            'text': 'A disk is rotating about a smooth fixed axis O, which passes through the center of the disk and is perpendicular to the plane of the disk, with an angular velocity in the direction shown in the diagram. If two equal forces F of opposite directions, but not along the same straight line, are simultaneously applied along the plane of the disk, as shown in the diagram, then the angular velocity w of the disk will:',
            'img': ['21.png'],
            'options': ['definitely increase', 'definitely decrease', 'remain unchanged', 'how it changes cannot be determined'],
            'answer': 'definitely increase', 'analysis': 'None'
        },
        {
            'id': 15,
            'text': 'A uniform thin rod OA can rotate around a smooth, horizontal fixed axis that is perpendicular to the rod and passes through one end O, as shown in the diagram. The rod is initially in a horizontal position and starts to fall freely from rest. As the rod swings to the vertical position, which of the following statements is correct?',
            'img': ['22.png'],
            'options': ['Angular velocity increases, angular acceleration decreases', 'Angular velocity increases, angular acceleration increases', 'Angular velocity decreases, angular acceleration decreases',
                        'Angular velocity decreases, angular acceleration increases'],
            'answer': 'Angular velocity increases, angular acceleration decreases', 'analysis': 'None'
        },
        {
            'id': 16,
            'text': 'Regarding the moment of inertia of a rigid body about an axis, which of the following statements is correct?',
            'options': [' It only depends on the mass of the rigid body and is independent of the mass distribution and the position of the axis', 'It depends on the mass and the mass distribution of the rigid body but is independent of the position of the axis', 'It depends on the mass, the mass distribution, and the position of the axis',
                        'It only depends on the position of the axis and is independent of the mass and mass distribution of the rigid body'],
            'answer': 'It depends on the mass, the mass distribution, and the position of the axis', 'analysis': 'None'
        },
        {
            'id': 17,
            'text': 'A light rope is wound around a fixed pulley with a horizontal axis. The moment of inertia of the pulley is J, and a mass mm is hanging from the rope. The gravitational force on the mass is P, and the angular acceleration of the pulley is a. If the mass is removed and a force equal to P is applied directly downward on the rope, the angular acceleration of the pulley will:',
            'options': ['remain unchanged', 'decrease', 'increase',
                        'how it changes cannot be determined'],
            'answer': 'increase', 'analysis': 'None'
        },
        {
            'id': 18,
            'text': 'A horizontal disk can rotate about a fixed vertical axis through its center, and a person is standing on the disk. Consider the person and the disk as a system. When the person walks freely on the disk, and assuming friction at the axis is negligible, which of the following is true for this system?',
            'options': ['Conservation of momentum', 'Conservation of mechanical energy','Conservation of angular momentum about the axis of rotation','Conservation of momentum, mechanical energy, and angular momentum', 'Conservation of neither momentum, mechanical energy, nor angular momentum'],
            'answer': 'Conservation of angular momentum about the axis of rotation', 'analysis': 'None'
        },
        {
            'id': 19,
            'text': 'A child with mass m is standing at the edge of a horizontal platform with radius R. The platform can rotate freely about a fixed smooth vertical axis through its center, with a moment of inertia J. Initially, both the platform and the child are at rest. When the child suddenly starts walking in a counterclockwise direction along the edge of the platform with a velocity v relative to the ground, what will be the angular velocity of the platform relative to the ground? ',
            'options': ['/static/imgs/23-1.png', '/static/imgs/23-2.png', '/static/imgs/23-3.png',
                        '/static/imgs/23-4.png'], 'answer': '/static/imgs/23-1.png', 'analysis': 'None'
        },
        {
            'id': 20,
            'text': 'The necessary and sufficient condition for the conservation of the angular momentum of a rigid body is:',
            'options': ['The rigid body is not subject to any external forces.','The resultant external torque on the rigid body is zero.'
            , 'The resultant external force and external torque on the rigid body are both zero.', 'The moment of inertia and angular velocity of the rigid body remain unchanged.'],
            'answer': 'The resultant external torque on the rigid body is zero.', 'analysis': 'None'
        },
        {
            'id': 21,
            'text': 'A person rides a bicycle westward at speed v, while the wind blows from 30° north-east at the same speed. From which direction does the person feel the wind blowing?',
            'options': ['30° north-east.','30° south-east.','30° north-west.','30° south-west.'],
            'answer': '30° north-west.', 'analysis': 'None'
        },
        {
            'id': 22,
            'text': 'A transverse wave propagates along the negative x-axis with speed u. The waveform at time t is shown in the figure. At this moment:',
            'img': ['24.png'],
            'options': ['The vibrational velocity at point A is positive.','Point B is stationary.' ,'Point C is moving downward.','The vibrational velocity at point D is negative.' ],
            'answer': 'The vibrational velocity at point D is negative. ', 'analysis': 'None'
        },
        {
            'id': 23,
            'text': 'The following function f (x,t) represents a one-dimensional wave in an elastic medium, where A、a and b are positive constants. Which function represents a traveling wave moving in the negative x-direction?',
            'options': ['/static/imgs/25-1.png', '/static/imgs/25-2.png', '/static/imgs/25-3.png',
                        '/static/imgs/25-4.png'],
            'answer': '/static/imgs/25-1.png', 'analysis': 'None'
        },
        {
            'id': 24,
            'text': 'A long rope is stretched horizontally, and one end is held by hand. Maintaining constant tension, if the end of the rope oscillates harmonically in a direction perpendicular to the rope:',
           'options': ['The higher the oscillation frequency, the longer the wavelength.' , 'The lower the oscillation frequency, the longer the wavelength.',' The higher the oscillation frequency, the faster the wave speed.','The lower the oscillation frequency, the faster the wave speed.'],
            'answer': 'The lower the oscillation frequency, the longer the wavelength.', 'analysis': 'None'
        },
        {
            'id': 25,
            'text': 'A transverse wave propagates along the negative x-axis. At time t, the waveform is as shown. At t + T /4, the vibrational displacements of points 1, 2, and 3 on the x-axis are:',
            'img': ['26.png'],
            'options': ['A,0,-A', '-A,0,A', '0,A,0', '0,-A,0'],
            'answer': '-A,0,A', 'analysis': 'None'
        },
        {
            'id': 26,
            'text': 'For a plane harmonic wave with a frequency of 100 Hz and propagation speed of 300 m/s, the phase difference between two points on the wave less than one wavelength apart is Pi/3 . The distance between these two points is:(only number,m)',
            'options': ['2.86', '2.19', '0.5', '0.25'],
            'answer': '0.5', 'analysis': 'Ppt 11'
        }
    ],

    'hard': [
        {
            'id': 27,
            'text': 'In Figure, a block of mass m = 3.20 kg slides from rest a distance d down a frictionless incline at angle θ = 30.0° where it runs into a spring of spring constant 431 N/m. When the block momentarily stops, it has compressed the spring by 21.0 cm. What are (a) distance d and (b) the distance between the point of the first block–spring contact and the point where the block’s speed is greatest?',
            'img': ['13.png'],
            'options': [], 'answer': ['0.396m', '3.64cm'], 'analysis': 'ppt 9'
        },
        {
            'id': 28,
            'text': 'In Figure, a 3.5 kg block is accelerated from rest by a compressed spring of spring constant 640 N/m. The block leaves the spring at the spring’s relaxed length and then travels over a horizontal floor with a coefficient of kinetic friction 𝜇k = 0.25. The frictional force stops the block in distance D = 7.8 m. What are (a) the increase in the thermal energy of the block–floor system, (b) the maximum kinetic energy of the block, and (c) the original compression distance of the spring?',
            'img': ['14.png'],
            'options': [], 'answer': ['67J', '67J', '0.46m'], 'analysis': 'ppt 9'
        },
        {
            'id': 29,
            'text': 'In Figure, what magnitude of (constant) force F → applied horizontally at the axle of the wheel is necessary to raise the wheel over a step obstacle of height h = 3.00 cm? The wheel’s radius is r = 6.00 cm, and its mass is m = 0.800 kg.(g=9.8N/kg)',
            'img': ['15.png'],
            'options': [], 'answer': ['13.6N'], 'analysis': 'ppt 9'},
        {
            'id': 30,
            'text': 'In Figure, a uniform plank, with a length L of 6.10 m and a weight of 445 N, rests on the ground and against a frictionless roller at the top of a wall of height h = 3.05 m. The plank remains in equilibrium for any value of θ ≥ 70° but slips if θ < 70°. Find the coefficient of static friction between the plank and the ground.',
            'img': ['16.png'],
            'options': [], 'answer': ['0.34'], 'analysis': 'ppt 3'},
        {
            'id': 31,
            'text': 'Several planets (Jupiter, Saturn, Uranus) are encircled by rings, perhaps composed of material that failed to form a satellite. In addition, many galaxies contain ring-like structures. Consider a homogeneous thin ring of mass M and outer radius R. (a) What gravitational attraction does it exert on a particle of mass m located on the ring’s central axis a distance x from the ring center? (b) Suppose the particle falls from rest as a result of the attraction of the ring of matter. What is the speed with which it passes through the center of the ring?',
            'img': ['17.png'],
            'options': [], 'answer': ['GMmx(x2+R2)-3/2; sqrt(2GM(1/R-1/sqrt(x2+R2)))'], 'analysis': 'ppt 11'},
        {
            'id': 31,
            'text': 'A uniform beam is 5.0 m long and has a mass of 53 kg. In the figure below, the beam is supported in a horizontal position by a hinge and a cable, with angle θ = 60°. In unit-vector notation, what is the horizontal force on the beam from the hinge?',
            'img': ['18.png'],
            'options': [], 'answer': ['299.9N'], 'analysis': 'Ppt 9'
        },
        {
            'id': 33,
            'text': 'Derive tidal force equation for a small object u on the moon m around the planet M: (See figure below for the meaning of symbols). And the Roche limit in which the u cannot stay on the moon’s surface:',
            'img': ['20.png'],
            'options': [], 'answer': [], 'analysis': 'Ppt 11'
        },
        {
            'id': 34,
            'text': 'A flywheel rotates at 600 rev/min with a moment of inertia of 2.5 kg·m2, A constant braking torque is applied to stop the flywheel within 1s. The magnitude of the constant braking torque M＝_____N*m',
            'options': [], 'answer': ['157'], 'analysis': 'None'
        },
        {
            'id': 35,
            'text': 'Two objects, with masses m and 2m (both treated as point masses), are connected by a light, rigid rod of length l. The system rotates about a fixed vertical axis O, which is perpendicular to the rod and passes through the rod. It is known that the distance from the axis O to the mass 2m is 1/3 l, and the linear velocity of the mass m is v, and the velocity is perpendicular to the rod. The magnitude of the angular momentum (torque) of the system is____________.',
            'img': ['26.png'],
            'options': [], 'answer': ['mvl'], 'analysis': 'None'
        },
        {
            'id': 36,
            'text': 'For a wave with a frequency of 500 Hz and a wave speed of 350 m/s, the distance between two points with a phase difference of 2/3 is _____m.',
            'options': [], 'answer': ['0.233'], 'analysis': 'None'
        },
        {
            'id': 37,
            'text': 'A plane simple harmonic wave has a wave speed of 6.0 m/s and a vibration period of 0.1 s. The wavelength is ______m. Along the wave propagation direction, two particles (distance between them is less than the wavelength) have a phase difference of 5Pi/6. The distance between these two particles is ______m. ',
            'options': [], 'answer': ['0.6','0.25'], 'analysis': 'None'
        },
        {
            'id': 38,
            'text': '5515: Points A and B are on the wave line of a simple harmonic wave. It is known that the vibration phase at point B lags behind Pi/3 that at point A, and the distance between A and B is 0.5 m. The wave frequency is 100 Hz. Then the wavelength = _______ m, and the wave speed u = _______ m/s. ',
            'options': [], 'answer': ['3','300'], 'analysis': 'None'
        },
        {
            'id': 39,
            'text': 'A particle moves in the Oxy-plane with kinematic equations x=2t and y=19-2t^2 (SI). The average speed of the particle during the second second V=_______m/s; and the instantaneous speed at the end of the second second  V2______m/s. ',
            'options': [], 'answer': ['6.32','8.25'], 'analysis': 'None'
        },
        {
            'id': 40,
            'text': 'An external horizontal force F presses object A against a vertical wall. Due to the friction between the object and the wall, the object remains stationary, with a static friction force f0 acting on it. If the external force is increased to 2F, the static friction force on the object becomes ________.',
            'img': ['28.png'],
            'options': [], 'answer': ['f0'], 'analysis': 'None'
        },
        {
            'id': 41,
            'text': 'As shown in the figure, a small object A rests against the vertical front wall of a small car. If the static friction coefficient between A and the car wall is us , then the minimum acceleration a required to prevent A from falling is ________.',
            'img': ['29.png'],
            'options': [], 'answer': ['g/us'], 'analysis': 'None'
        },
        {
            'id': 42,
            'text': 'A pile driver has a mass of m1, and the pile has a mass of m2. Assuming a completely inelastic collision occurs during the very short time they collide, the kinetic energy of the pile and pile driver just after the collision is _______ times the initial kinetic energy of the pile driver.',
            'options': [], 'answer': ['m1/(m1+m2)'], 'analysis': 'None'
        }
    ],
}

scores = {}
scoreList = []


@app.route('/', methods=['GET'])
def index():
    return render_template('web.html')


@app.route('/login', methods=['GET'])
def login():
    return render_template('index.html')


@app.route('/quiz', methods=['GET'])
def quiz():
    return render_template('quiz.html')


@app.route('/question', methods=['GET'])
def get_question():
    difficulty = request.args.get('difficulty', 'medium')
    user_id = request.args.get('userId')
    question_list = questions.get(difficulty, [])

    if user_id not in scores:
        scores[user_id] = {'easy': 100, 'easyCount': 0, 'easyTrueCount': 0, 'medium': 100, 'mediumCount': 0,
                           'mediumTrueCount': 0, 'hard': 100, 'hardCount': 0, 'hardTrueCount': 0}

    user = any(score['userId'] == user_id for score in scoreList)
    if not user:
        scoreList.append({
            'userId': user_id,
            'easy': {
                'true': 0,
                'count': 0,
                'score': 100
            },
            'medium': {
                'true': 0,
                'count': 0,
                'score': 100
            },
            'hard': {
                'true': 0,
                'count': 0,
                'score': 100
            }
        })

    if question_list:
        random_question = random.choice(question_list)
        scores[user_id][difficulty + 'Count'] += 1
        for score in scoreList:
            if score['userId'] == user_id:
                score[difficulty]['count'] += 1
                break
        return jsonify(random_question)
    else:
        return jsonify({'error': 'Invalid difficulty level'}), 400


@app.route('/update-score', methods=['POST'])
def update_score():
    data = request.json
    user_id = data.get('userId')
    difficulty = data.get('difficulty')
    is_correct = data.get('isCorrect')

    if not is_correct:
        scores[user_id][difficulty] = max(0, scores[user_id][difficulty] - 5)
        for score in scoreList:
            if score['userId'] == user_id:
                score[difficulty]['score'] = max(0, score[difficulty]['score'] - 5)
                break
    else:
        scores[user_id][difficulty + 'TrueCount'] += 1
        for score in scoreList:
            if score['userId'] == user_id:
                score[difficulty]['true'] += 1
                break

    return jsonify({'status': 'success'})


@app.route('/scores', methods=['GET'])
def scores_view():
    return jsonify(scores)


if __name__ == '__main__':
    app.run(debug=True)
