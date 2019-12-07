% GA-VF-add

root1 = ['/Users/wangyipeng/Desktop/20190121-GA-VFGA/数据统计/vf-ga-add/for_matlab/'];

a1 = importdata([root1 '0.2_20.txt']);
b1 = importdata([root1 '0.2_200.txt']);
c1 = importdata([root1 '2_20.txt']);
d1 = importdata([root1 '2_200.txt']);

a=a1(:,5);
b=b1(:,5);
c=c1(:,5);
d=d1(:,5);

index = 0:1:500;

figure
hold on
p_a = plot(index, a(1:1:501),'r');
p_b = plot(index, b(1:1:501),'g');
p_c = plot(index, c(1:1:501),'b');
p_d = plot(index, d(1:1:501),'y');
legend([p_a,p_b,p_c,p_d],'w_\alpha=0.2  w_\beta=20','w_\alpha=0.2  w_\beta=200','w_\alpha=2     w_\beta=20','w_\alpha=2     w_\beta=200')

