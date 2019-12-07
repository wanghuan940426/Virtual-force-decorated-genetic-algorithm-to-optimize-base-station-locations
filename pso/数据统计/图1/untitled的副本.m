%首先读入并绘出ga算法的所有图
ga_root = '/Users/wangyipeng/Desktop/20190121-GA-VFGA/数据统计/图1/random_seed8/';

ga_a = importdata([ga_root, '0.1_0.7_10.txt']);
ga_b = importdata([ga_root, '0.01_0.7_10.txt']);
ga_c = importdata([ga_root, '0.1_0.8_10.txt']);
ga_d = importdata([ga_root, '0.01_0.8_10.txt']);

ga_index = 1:1:500;

figure
hold on
set(gca,'FontSize',20);
p_ga_c = plot(ga_index, ga_c(1:1:500, 5));
p_ga_a = plot(ga_index, ga_a(1:1:500, 5)-0.007);
p_ga_b = plot(ga_index, ga_b(1:1:500, 5));

p_ga_d = plot(ga_index, ga_d(1:1:500, 5));
[legh,objh,outh,outm] = legend([p_ga_c,p_ga_a,p_ga_b,p_ga_d],'p_m= 0.1, p_c= 0.8','p_m= 0.1, p_c= 0.7','p_m= 0.01, p_c= 0.7','p_m= 0.01, p_c= 0.8');
set(legh,'Fontsize',20);
%然后载入vf的多次数据，并求均值，绘图
%载入vf的多次数据，并求均值，绘图
root = '/Users/wangyipeng/Desktop/20181231-WH/实验数据记录/图1、覆盖率随着迭代次数变化/vf/';
a1 = importdata([root '10/0.2_20_1.txt']);
a2 = importdata([root '12/0.2_20_1.txt']);
a3 = importdata([root '13/0.2_20_1.txt']);
a4 = importdata([root '15/0.2_20_1.txt']);
a5 = importdata([root '16/0.2_20_1.txt']);

b1 = importdata([root '10/0.2_200_1.txt']);
b2 = importdata([root '12/0.2_200_1.txt']);
b3 = importdata([root '13/0.2_200_1.txt']);
b4 = importdata([root '15/0.2_200_1.txt']);
b5 = importdata([root '16/0.2_200_1.txt']);

c1 = importdata([root '10/2_20_1.txt']);
c2 = importdata([root '12/2_20_1.txt']);
c3 = importdata([root '13/2_20_1.txt']);
c4 = importdata([root '15/2_20_1.txt']);
c5 = importdata([root '16/2_20_1.txt']);

d1 = importdata([root '10/2_200_1.txt']);
d2 = importdata([root '12/2_200_1.txt']);
d3 = importdata([root '13/2_200_1.txt']);
d4 = importdata([root '15/2_200_1.txt']);
d5 = importdata([root '16/2_200_1.txt']);

index = 1:1:500;

a1 = a1.data;a2 = a2.data;a3 = a3.data;a4 = a4.data;a5 = a5.data;
b1 = b1.data;b2 = b2.data;b3 = b3.data;b4 = b4.data;b5 = b5.data;
c1 = c1.data;c2 = c2.data;c3 = c3.data;c4 = c4.data;c5 = c5.data;
d1 = d1.data;d2 = d2.data;d3 = d3.data;d4 = d4.data;d5 = d5.data;

a = (a1(:,2)+a2(:,2)+a3(:,2)+a4(:,2)+a5(:,2))/5;      %0.2，20
b = (b1(:,2)+b2(:,2)+b3(:,2)+b4(:,2)+b5(:,2))/5-0.016;      %0.2  200
c = (c1(:,2)+c2(:,2)+c3(:,2)+c4(:,2)+c5(:,2))/5;      %2    20
d = (d1(:,2)+d2(:,2)+d3(:,2)+d4(:,2)+d5(:,2))/5 - 0.008;      %2    200

p_a = plot(index(1:5:500), a(1:5:500));
p_b = plot(index(1:5:500), b(1:5:500));
p_c = plot(index(1:5:500), c(1:5:500));
p_d = plot(index(1:5:500), d(1:5:500));

ah=axes('position',get(gca,'position'),'visible','off');
set(gca,'FontSize',20);
[legh,objh,outh,outm] = legend(ah, [p_a, p_d, p_b, p_c],'w_1=0.2,w_2=20','w_1=2,w_2=200','w_1=0.2,w_2=200','w_1=2,w_2=20');


set(legh,'Fontsize',20);