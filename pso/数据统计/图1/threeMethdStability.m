% GA-OLD
NAME = {'GA-Old/', 'GA-NEW/', 'GA-VF/'};
IDX = 1;
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

index = 0:1:500;

a = (a1(1:1:501,5)+a2(1:1:501,5)+a3(1:1:501,5)+a4(1:1:501,5)+a5(1:1:501,5))/5;      %0.1   0.7
atmp = [a1(1:1:501,5) a2(1:1:501,5) a3(1:1:501,5) a4(1:1:501,5) a5(1:1:501,5)];
aMax = max(atmp, [], 2);
aMin = min(atmp, [], 2);

% GA-NEW
IDX = 2;
root1 = ['/Users/wangyipeng/Desktop/20190121-GA-VFGA/数据统计/图1/random_seed8/forMatlab/',NAME{IDX}];
root2 = ['/Users/wangyipeng/Desktop/20190121-GA-VFGA/数据统计/图1/random_seed18/forMatlab/',NAME{IDX}];
root3 = ['/Users/wangyipeng/Desktop/20190121-GA-VFGA/数据统计/图1/random_seed28/forMatlab/',NAME{IDX}];
root4 = ['/Users/wangyipeng/Desktop/20190121-GA-VFGA/数据统计/图1/random_seed38/forMatlab/',NAME{IDX}];
root5 = ['/Users/wangyipeng/Desktop/20190121-GA-VFGA/数据统计/图1/random_seed48/forMatlab/',NAME{IDX}];

c1 = importdata([root1 '0.1_0.8_10.txt']);
c2 = importdata([root2 '0.1_0.8_10.txt']);
c3 = importdata([root3 '0.1_0.8_10.txt']);
c4 = importdata([root4 '0.1_0.8_10.txt']);
c5 = importdata([root5 '0.1_0.8_10.txt']);

b = (c1(1:1:501,5)+c2(1:1:501,5)+c3(1:1:501,5)+c4(1:1:501,5)+c5(1:1:501,5))/5;      %0.1   0.8
btmp = [c1(1:1:501,5),c2(1:1:501,5),c3(1:1:501,5),c4(1:1:501,5),c5(1:1:501,5)];
bMax = max(btmp, [], 2);
bMin = min(btmp, [], 2);

% GA-VF
IDX = 3;
root1 = ['/Users/wangyipeng/Desktop/20190121-GA-VFGA/数据统计/图1/random_seed8/forMatlab/',NAME{IDX}];
root2 = ['/Users/wangyipeng/Desktop/20190121-GA-VFGA/数据统计/图1/random_seed18/forMatlab/',NAME{IDX}];
root3 = ['/Users/wangyipeng/Desktop/20190121-GA-VFGA/数据统计/图1/random_seed28/forMatlab/',NAME{IDX}];
root4 = ['/Users/wangyipeng/Desktop/20190121-GA-VFGA/数据统计/图1/random_seed38/forMatlab/',NAME{IDX}];
root5 = ['/Users/wangyipeng/Desktop/20190121-GA-VFGA/数据统计/图1/random_seed48/forMatlab/',NAME{IDX}];

c1 = importdata([root1 '0.1_0.8_10.txt']);
c2 = importdata([root2 '0.1_0.8_10.txt']);
c3 = importdata([root3 '0.1_0.8_10.txt']);
c4 = importdata([root4 '0.1_0.8_10.txt']);
c5 = importdata([root5 '0.1_0.8_10.txt']);

c = (c1(1:1:501,5)+c2(1:1:501,5)+c3(1:1:501,5)+c4(1:1:501,5)+c5(1:1:501,5))/5;      %0.1   0.8
ctmp = [c1(1:1:501,5),c2(1:1:501,5),c3(1:1:501,5),c4(1:1:501,5),c5(1:1:501,5)];
cMax = max(ctmp, [], 2);
cMin = min(ctmp, [], 2);


figure
hold on
%p_a = plot(index, a(1:1:501));
%p_aMax = plot(index, aMax(1:1:501));
%p_aMin = plot(index, aMin(1:1:501));
%p_b = plot(index, b(1:1:501));
%p_bMax = plot(index, bMax(1:1:501));
%p_bMin = plot(index, bMin(1:1:501));
%p_c = plot(index, c(1:1:501));
%p_cMax = plot(index, cMax(1:1:501));
%p_cMin = plot(index, cMin(1:1:501));
%legend([p_a,p_b,p_c],'Ga-Old','Ga-New','GA-VF')
for idx=1:1:500
    plot([idx, idx], [aMax(idx), aMin(idx)],'g')
    pause(0.01)
end

for idx=1:1:500
    plot([idx, idx], [bMax(idx), bMin(idx)],'b')
    pause(0.01)
end

for idx=1:1:500
    plot([idx, idx], [cMax(idx), cMin(idx)],'r')
    pause(0.01)
end

p_a = plot(index, a(1:1:501),'g','LineWidth',5);
pause(0.5)
p_b = plot(index, b(1:1:501),'b','LineWidth',5);
pause(0.5)
p_c = plot(index, c(1:1:501),'r','LineWidth',5);
legend([p_c,p_b,p_a],'VF-GA','Norm-GA','GA')