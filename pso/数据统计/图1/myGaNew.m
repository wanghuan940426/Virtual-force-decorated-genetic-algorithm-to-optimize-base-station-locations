% GA-Old
NAME = {'GA-Old/', 'GA-NEW/', 'GA-VF/'};
IDX = 2;
root1 = ['/Users/wangyipeng/Desktop/20190121-GA-VFGA/数据统计/图1/random_seed8/forMatlab/',NAME{IDX}];
root2 = ['/Users/wangyipeng/Desktop/20190121-GA-VFGA/数据统计/图1/random_seed18/forMatlab/',NAME{IDX}];
root3 = ['/Users/wangyipeng/Desktop/20190121-GA-VFGA/数据统计/图1/random_seed28/forMatlab/',NAME{IDX}];
root4 = ['/Users/wangyipeng/Desktop/20190121-GA-VFGA/数据统计/图1/random_seed38/forMatlab/',NAME{IDX}];
root5 = ['/Users/wangyipeng/Desktop/20190121-GA-VFGA/数据统计/图1/random_seed48/forMatlab/',NAME{IDX}];

a1 = importdata([root1 '0.1_0.7_10.txt']);
a2 = importdata([root2 '0.1_0.7_10.txt']);
a3 = importdata([root3 '0.1_0.7_10.txt']);
a4 = importdata([root4 '0.1_0.7_10.txt']);
a5 = importdata([root5 '0.1_0.7_10.txt']);

b1 = importdata([root1 '0.01_0.7_10.txt']);
b2 = importdata([root2 '0.01_0.7_10.txt']);
b3 = importdata([root3 '0.01_0.7_10.txt']);
b4 = importdata([root4 '0.01_0.7_10.txt']);
b5 = importdata([root5 '0.01_0.7_10.txt']);

c1 = importdata([root1 '0.1_0.8_10.txt']);
c2 = importdata([root2 '0.1_0.8_10.txt']);
c3 = importdata([root3 '0.1_0.8_10.txt']);
c4 = importdata([root4 '0.1_0.8_10.txt']);
c5 = importdata([root5 '0.1_0.8_10.txt']);

d1 = importdata([root1 '0.01_0.8_10.txt']);
d2 = importdata([root2 '0.01_0.8_10.txt']);
d3 = importdata([root3 '0.01_0.8_10.txt']);
d4 = importdata([root4 '0.01_0.8_10.txt']);
d5 = importdata([root5 '0.01_0.8_10.txt']);

index = 0:1:500;

a = (a1(1:1:501,5)+a2(1:1:501,5)+a3(1:1:501,5)+a4(1:1:501,5)+a5(1:1:501,5))/5;      %0.1   0.7
b = (b1(1:1:501,5)+b2(1:1:501,5)+b3(1:1:501,5)+b4(1:1:501,5)+b5(1:1:501,5))/5;      %0.01  0.7
c = (c1(1:1:501,5)+c2(1:1:501,5)+c3(1:1:501,5)+c4(1:1:501,5)+c5(1:1:501,5))/5;      %0.1   0.8
d = (d1(1:1:501,5)+d2(1:1:501,5)+d3(1:1:501,5)+d4(1:1:501,5)+d5(1:1:501,5))/5;      %0.01  0.8

figure
hold on
p_a = plot(index, a(1:1:501),'r');
p_b = plot(index, b(1:1:501),'g');
p_c = plot(index, c(1:1:501),'b');
p_d = plot(index, d(1:1:501),'y');
legend([p_a,p_b,p_c,p_d],'p_m=0.1    p_c=0.7','p_m=0.01   p_c=0.7','p_m=0.1    p_c=0.8','p_m=0.01   p_c=0.8')
