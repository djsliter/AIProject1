import math

import pygame

import gui_game

# up = 0, right = 1, down = 2, left = 3

# delta_up delta_down delta_left delta_right
# last_ate_time body_in_way up_safe down_safe
# left_safe right_safe

individual = [-0.2909073, 0.4498955, 0.10807185, 0.103604145, 0.36366224, 0.28103197, -0.3277357, -0.044263575, 0.35423225, -0.29384932, 0.09201274, -0.516634, -0.048568714, 0.44422174, -0.19661088, 0.48293665, -0.23972827, 0.36357045, 0.3745625, 0.8212157, 0.2838744, -0.21656425, 0.2718894, 0.3298144, 0.13306072, -0.22420959, 0.33390996, -0.24910259, 0.2947972, -0.053024206, 0.1443444, 0.2420171, 0.29679552, 0.45172888, 0.100141615, 0.26491722, 0.32749635, 0.15684813, 0.18008347, -0.47215992, 0.029633192, -0.011844025, 0.3110383, 0.20993266, -0.052712303, -0.53411573, 0.20011587, 0.39686635, -0.24452004, -0.0952771, -0.07120773, 0.124004096, 0.27454513, 0.16701679, -0.097310044, 0.020661011, -0.07847537, 0.17363207, 0.124207996, -0.24931444, 0.28701234, 0.2308253, 0.47784138, -0.06502473, 0.094462514, 0.41731095, 0.2632358, 0.33347094, -0.41850936, -0.23565888, -0.1662426, 0.01748681, 0.1649369, -0.26001242, 0.073475435, 0.15114978, -0.12078571, -0.37902763, 0.29627907, 0.6548594, 0.32771808, -0.057565674, -0.25774497, -0.42179066, 0.4381857, -0.042056885, -0.11534312, 0.30980656, 0.42034635, 0.76437956, -0.33089408, 0.82167083, -0.10817338, -0.1590283, 0.20498255, 0.31180373, 0.5385884, -0.35292634, -0.33334497, 0.042821046, -0.22711942, 0.47682884, -0.37658, 0.25041845, -0.30177143, -0.124177024, 0.11793433, -0.45608693, -0.30266273, 0.224463, 0.54685235, 0.32032725, -0.25230697, -0.13224931, 0.47173733, -0.147486, 0.16467, 0.41723126, -0.024250152, 0.30831704, 0.33266696, 0.30740973, 0.5173825, -0.1525037, 0.021661976, -0.52097005, -0.019134805, -0.39270422, 0.46883228, 0.15552144, 0.37025556, -0.041253697, -0.15165901, -0.5118416, -0.32079992, 0.44847584, -0.17146, 0.32355076, 0.48423326, -0.105371624, 0.32386753, 0.04058301, -0.25066137, -0.23096886, -0.37200704, 0.21852414, -0.1787061, 0.042842936, 0.21087658, -0.12507698, -0.017143287, -0.025979578, 0.46102268, 0.0067147356, 0.43107885, -0.2155925, 0.19850016, -0.3040508, 0.2591559, 0.41310346, 0.54129696, 0.16344714, -0.00097448524, -0.029893365, -0.06538705, 0.2799073, 0.46720967, 0.17073119, 0.094801225, -0.42142722, 0.08871173, -0.15616746, 0.28424534, 0.25705835, 0.32408002, -0.14362612, 0.27719074, -0.0013137459, 0.013875588, 0.18432459, 0.35030335, -0.10758324, -0.06781484, 0.23093572, -0.20721285, 0.20339741, 0.29962322, -0.3010152, 0.083961785, 0.2636789, 0.25365022, 0.2784384, 0.36495242, 0.43023407, -0.42262465, 0.028366543, 0.45433372, -0.04542908, 0.002228497, 0.03814355, -0.33443382, -0.0870705, -0.62522364, -0.03621465, 0.25627914, -0.005482286, -0.06795005, -0.38055757, -0.14150566, 0.022558134, 0.12766242, 0.61124426, -0.13524929, -0.17450728, 0.13436246, -0.076673985, 0.0045358827, 0.31949037, 0.05474049, 0.4546963, -0.21231633, 0.013959587, -0.33450267, -0.095596105, 0.1907548, 0.1185413, -0.20227085, -0.2503188, 0.4134886, 0.030161949, 0.36406893, 0.16109878, -0.02663533, 0.11285766, 0.24949817, 0.28204432, 0.9907634, -0.14202437, -0.1400011, -0.41240197, -0.24524926, -0.26107585, 0.39044085, 0.36257464, -0.16734947, 0.4896021, -0.34354463, -0.11999396, -0.09034616, 0.25670952, -0.24070391, -0.5193024, 0.35405046, 0.026902325, -0.46846652, 0.25149533, -0.14684682, -0.34771428, 0.19726132, -0.32100773, 0.268245, 0.15570357, 0.3552338, 0.22367296, -0.19067593, 0.24826191, -0.02752319, 0.23511346, 0.07584119, -0.34182438, 0.200285, 0.1112082, -0.05866738, 0.35227627, -0.26885477, -0.23552087, 0.10848412, -0.23988307, 0.3774327, 0.2802855, 0.21127109, -0.032747094, -0.24407029, 0.72380865, -0.22128601, 0.40029284, 0.47523427, -0.39241397, -0.088821664, -0.07853117, -0.12720273, -0.29409355, 0.038192187, -0.38843778, 0.28587756, 0.24854773, -0.14421229, -0.22983876, 0.21412559, -0.0010224286, -0.27693602, 0.12719813, -0.35236138, -0.014091027, 0.08729932, 0.37178367, 0.395528, 0.03980168, -0.40976906, 0.033597663, 0.14952819, 0.43445468, 0.1710041, 0.31546617, -0.071259454, 0.109538205, -0.049082126, -0.3157654, 0.52640355, 0.585204, -0.24744993, -0.04807475, 0.0076810615, 0.63674384, 0.4300636, 0.41766933, 0.17001675, 0.21722803, 0.15127014, 0.294417, -0.2536737, -0.34968203, -0.13449101, 0.3933447, -0.42650962, 0.12546045, -0.117490605, 0.18170623, 0.2862267, 0.41761273, 0.44431618, 0.1865351, 0.14401306, -0.017631918, 0.19714448, -0.14762935, 0.045366287, -0.022832142, 0.1517464, -0.26065278, 0.1672622, -0.24227343, 0.35674778, -0.31628883, 0.16752388, 0.1896539, -0.25321707, -0.29929814, -0.15640007, 0.14802688, 0.16546194, -0.033739004, 0.379077, -0.2872954, -0.21954465, -0.08619341, -0.14675276, -0.33454037, 0.27094534, -0.08807814, 0.16604395, 0.15647449, -0.26087248, 0.019207519, -0.32105735, -0.08568345, 0.25600648, 0.43752974, 0.33251724, -0.06505994, -0.43495274, -0.30305845, 0.25355235, -0.0798198, -0.23012403, 0.31935403, 0.3468526, 0.13174653, -0.031346202, 0.5121709, -0.017499028, 0.5574386, -0.19040626, 0.053214166, 0.07931223, -0.39232007, 0.039667953, 0.13193616, -0.34194022, -0.36397323, 0.2869588, 0.22463262, 0.17333047, 0.2938715, 0.5717102, 0.25838855, 0.3679485, 0.386645, 0.10871593, 0.24735801, -0.23435082, -0.22574152, 0.17617694, 0.15590286, -0.3984476, -0.1524871, 0.41751182, -0.2957635, 0.44815055, -0.12197526, 0.15244517, 0.11392961, -0.34741783, -0.24044353, -0.1305399, -0.0074971616, 0.17090857, 0.008088062, 0.016027143, -0.41208237, 0.15753616, -0.05289627, 0.18171288, 0.020125885, -0.2861936, 0.05059769, -0.15283038, 0.048521478, -0.16499168, -0.103236735, 0.22251868, 0.112234734, 0.18869305, -0.30800623, -0.011343599, -0.04543637, -0.1477426, -0.5055043, 0.19641683, -0.1024165, -0.04900996, 0.3520939, -0.32384223, 0.38167128, 0.30988222, 0.18448506, 0.30833456, -0.015778512, -0.20668828, -0.14910218, 0.21641114, 0.11669198, 0.17251715, 0.0002362132, 0.051317483, -0.2871619, -0.35614592, 0.3702967, -0.29944766, 0.2940736, -0.22989057, 0.0814549, -0.12076641, 0.28976443, 0.28267536, 0.39319086, -0.2442921, 0.39229926, -0.0932706, 0.3904823, 0.07650763, -0.25605416, 0.34610283, 0.22133714, 0.09984005, -0.10622795, 0.043834485, -0.27809104, -0.3778762, 0.89879644, 0.19413945, -0.6524968, -0.17651343, -0.2644308, 0.30091587, -0.105941474, -0.26093346, -0.0896174, -0.05584024, -0.3550152, -0.23418808, -0.17579196, 0.09997713, -0.31113753, -0.08957809, -0.24051346, 0.2419178, 0.30680305, 0.26017007, -0.1353268, -0.16555129, 0.14610542, 0.039636593, -0.44604307, 0.3220277, -0.020700544, -0.30820537, 0.11660362, -0.22252369, 0.27155793, 0.34193453, -0.048057977, 0.065109834, 0.13012078, 0.010660473, -0.18201596, 0.02972413, -0.48372227, 0.10055225, 0.21870928, 0.45700565, 0.6609924, 0.14604828, 0.27592066, 0.16679989, -0.35693046, 0.072767384, 0.19164327, 0.43278673, -0.29973215, 0.42168695, -0.28546813, -0.26619074, 0.2547604, 0.31278968, -0.015044508, -0.3368611, -0.008257955, -0.42872438, 0.2871546, 0.32519957, -0.06233701, 0.2330685, 0.29677868, -0.22486494, 0.08041885, -0.27537182, -0.25583744, -0.41341078, -0.17099386, 0.37815985, -0.3458961, 0.16717385, 0.35588816, -0.40146598, 0.283375, -0.119290374, 0.3619757, -0.09710048, 0.19478121, -0.14453349, 0.29322344, 0.2923259, 0.27145115, -0.22546527, -0.31470188, 0.3694808, -0.4045367, -0.0038192235, -0.4244146, 0.12959537, 0.050618228, -0.0010262175, -0.33216, 0.061148364, -0.042066634, 0.4015368, -0.5197424, -0.23749304, 0.21171495, 0.09926883, -0.116177484, 0.001498015, -0.41669518, 0.47118166, 0.11031069, 0.29260924, -0.41618833, -0.42522058, -0.009991631, 0.20882975, 0.09745806, 0.35397473, 0.3830047, -0.1868409, -0.17075942, -0.009512343, -0.24212916, 0.4174166, 0.08806224, -0.17340696, -0.06735131, -0.28031194, 0.30712485, -0.17434315, -0.23982754, -0.085083574, -0.24998504, -0.51068336, 0.10097957, 0.081275165, -0.4287433, -0.02348486, -0.004834223, 0.22550523, 0.14586692, -0.34098834, -0.40461183, -0.4114179, -0.4039584, -0.017571399, 0.6002969, -0.07212892, 0.18874156, 0.14340906, 0.3494518, -0.18726596, 0.03527164, -0.10217725, -0.44587395, -0.24307671, -0.054656386, -0.34235033, -0.111957744, -0.16249445, 0.40372145, -0.075399905, -0.018592358, -0.11262742, 0.29843622, -0.08914024, 0.27712, 0.011238039, -0.29741818, 0.49095604, -0.17038961, 0.3097126, 0.3946207, -0.44605023, 0.59041137, 0.16463661, 0.40252858, 0.11831159, -0.055350095, -0.43324924, 0.41489056, 0.12803046, -0.1491209, -0.11217108, -0.31350917, 0.3065511, 0.20737551, -0.31288403, 0.44268394, -0.3560864, 0.006866076, 0.1302486, 0.39464533, 0.054399703, 0.17710297, -0.33104667, -0.39488614, -0.44818366, 0.58777744, -0.09143171, 0.13807338, -0.5019367, 0.40214652, -0.21731085, -0.19044322, 0.5056687, 0.5024964, 0.20307165, -0.022194726, 0.0006085711, 0.6026367, -0.47387114, 0.10417339, 0.15962622, 0.6736779, 0.12765789, 0.27747107, 0.15942253, 0.21284807, 0.119143784, 0.342836, 0.27586985, 0.63071424, -0.18522573, -0.18053941, 0.40205166, -0.25326365, -0.41659552, 0.18927597, -0.22923899, -0.5331749, -0.43821755, 0.3260162, -0.51219356, 0.31227398, 0.3580733, 0.28761882, -0.19210368, 0.39205745, -0.3523994, 0.5431419, 0.6292648, 0.35779756, -0.17719126, -0.5977483, 0.17174435, 0.020363303, -0.59181476, -0.34997076, -0.53171355, 0.61296886, 0.28294188, 0.8400365, 0.3099578, 0.14781788, -0.47405797, 0.52930015, -0.40338427, -0.15376318, -0.68136364, -0.15281555, -0.07487856, 0.9816538, 0.028416276, -0.38164744, -0.23647654, -0.31031436, -0.3159756, 0.13061473, 0.2703351, 0.19493107]

game1 = gui_game.SnakeGame(120, individual, 12, 12, 8, 1, pygame)
game1.runGame()
food_score = math.sqrt(math.pow(game1.score, 3)) * 600  # weigh picking up more food heavily

time_score = game1.total_ticks  # use time in seconds as survival

print(food_score + time_score)