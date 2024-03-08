"""Main module for trying out code ideas
"""

# ! Implement testing procedures - preferably using 'pytest'
# ? Should we implement a CoonsPatch.__init__ which checks if curves are valid
# ? Should we implement a Density(DistMethod) class that uses Curve.get_length() <- might not work..
# ? Should we use pydoc or mkdoc to generate code documentation??
# BUG: Arc3 not implemented yet...

from matplotlib import pyplot as plt

from gdfgen import Point, Line, Arc3, CoonsPatch, Linear, CosineBoth, CosineEnd1, CosineEnd2

point_bl = Point(0, 0, 0)
point_br = Point.set_relative_to(point_bl, dx=1.0)
point_tr = Point(1, 1, 0)
point_tl = Point(0, 1, 0)

#for point in [point_bl, point_tl, point_tr, point_tl]:
#    print(point)
#print()

line1 = Line(point_bl, point_br)# pu0
#line2 = Line(point_tl, point_tr)# pu1
line2 = Arc3(point_tl, point_tr, Point(0.5, 0.0, 0.0))# pu1
line3 = Line(point_bl, point_tl)# p0w
line4 = Line(point_br, point_tr)# p1w

#for line in [line1, line2, line3, line4]:
#    print(line)
#print()

#dist = Point.get_distance(point_bl, point_br)
#print(dist)

surface1 = CoonsPatch(line1, line2, line3, line4)
surface1.set_dist_methods(dist_u1=CosineBoth)
surface1.set_num_points(num_points_u=20, num_points_w=20)
surface1_mp = surface1.mesh_points

plt.close("all")
plt.style.use('dark_background')
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
for i in range(0, 20):
    for j in range(0, 20):
        ax.scatter(surface1_mp[0,i,j], surface1_mp[1,i,j], surface1_mp[2,i,j], color='blue')
ax.set_xlabel('x (m)')
ax.set_ylabel('y (m)')
ax.set_zlabel('z (m)')
ax.view_init(azim=270, elev=90)
plt.show()
