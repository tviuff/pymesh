"""Main module for trying out code ideas
"""

from matplotlib import pyplot as plt

from mesh_generator import Point, Line, CoonsPatch

point_bl = Point(0, 0, 0)
point_br = Point.set_point_relative_to(point_bl, dx=1.0)
point_tr = Point(1, 1, 0)
point_tl = Point(0, 1, 0)

#for point in [point_bl, point_tl, point_tr, point_tl]:
#    print(point)
#print()

line1 = Line(point_bl, point_br)# pu0
line2 = Line(point_tl, point_tr)# pu1
line3 = Line(point_bl, point_tl)# p0w
line4 = Line(point_br, point_tr)# p1w

#for line in [line1, line2, line3, line4]:
#    print(line)
#print()

#line1.print_mesh_dist_option_list()
#print()
#line1_mesh = line1.generate_mesh_points(num_points=0, option="linear")

#print(line1_mesh)
#print()

#dist = Point.get_distance(point_bl, point_br)
#print(dist)

surface1 = CoonsPatch(line1, line2, line3, line4)
surface1.generate_mesh_points(
    num_points_u=20, num_points_w=20,
    option_u0='linear', option_0w='linear',
    option_u1='cosine_both', option_1w='linear'
    )
surface1_mesh = surface1.get_mesh_points()

plt.close("all")
plt.style.use('dark_background')
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
for i in range(0, 20):
    for j in range(0, 20):
        ax.scatter(surface1_mesh[0,i,j], surface1_mesh[1,i,j], surface1_mesh[2,i,j], color='blue')
ax.set_xlabel('x (m)')
ax.set_ylabel('y (m)')
ax.set_zlabel('z (m)')
ax.view_init(azim=270, elev=90)
plt.show()
