#include "predict.h"
#include <stdio.h>

/*Add*/
#include <string.h>
//#include <string>
#include <time.h>
#include <stdlib.h>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include <iterator>
#include <map>
#include <math.h>

/*************** WAN  ***********************/
//回归代码 
#ifdef _LINEREG
#define   LParaNum    2                         //回归参数个数
#endif
/*******************************************/

using namespace std;



//日期结构体
struct Data {
	int year;
	int month;
	int day;
	};

//input虚拟机结构体
struct Flaln
	{
	string type;     //虚拟机类型
	int par[2];    //par[0]:cpu   par[1]:memory
	vector<int> num;  //建立动态数组，InputFlavor[i].num[j]:第i种虚拟机在第j天的使用数量
	int total;   //预测时间段该种虚拟机访问数量的总和
	int rest;    //配置后剩余的该种虚拟机数量
	int SingleVmFlag;   //在单台服务器上放置许可开关   为0时不能再在该服务器上放置  为1时能在该服务器上放置
	};

//TrainData信息结构体
struct FlaTD {
	string type;
	Data data;
	};

//设置input给的物理服务器的参数   //这里也可以简化代码
struct Server
{
	int par[2];  //par[0]:CPU核数   par[1]:内存大小
	vector<int> flavor;  //flavor[0]表示要放的第1种虚拟机的台数，这里用下标直接代替了虚拟机种类，很明显可以flavor.resize(InputNum)
};


/*************** WAN  ***********************/
//线性回归方程参数 存储数组
#ifdef _LINEREG
double LinePara[LParaNum];                       //回归用参数
#endif
/*******************************************/



//读取单条TrainData
FlaTD ReadSingleTrainData(const string flavor)
{
	FlaTD fla;
	istringstream is(flavor);
	string s;
	int flag = 0;
	while (is >> s && flag < 3)
	{
		switch (flag)
		{
			case 0:    //跳过用户名
				{
				flag++;
				break;
				}
			case 1:    //存储flavor类型
				{
				fla.type = s;
				flag++;
				break;
				}
			case 2:   //存储日期
				{
				char *cha = (char*)s.data();
				sscanf(cha, "%d-%d-%d", &fla.data.year, &fla.data.month, &fla.data.day);
				flag++;
				break;
				}
		}
	}
	return fla;
}

//读取物理服务器CPU和内存
void ReadPhysicsPar(string tmp, int par[])
{
	istringstream is(tmp);
	string s;
	int flag = 0;
	while (is >> s)
	{
	    switch (flag)
		{
		    case 0:    //存储CPU
			{
			    par[0] = atoi(s.c_str());
			    flag++;
			    break;
			}
		    case 1:    //存储内存
			{
			    par[1] = atoi(s.c_str());
			    flag++;
			    break;
			}
		}
	}
}

//读取待优化的资源类型
int ReadTypeToOptimize(string tmp)
{
    int flag = 1;
    if (tmp == "CPU")
		flag = 0;
	return flag;
}

//读取待预测两个时间点
Data ReadFlagDay(string tmp)
{
	Data tmp_data = {0,0,0};
	istringstream is(tmp);
	string s;
	int flag = 0;
	while (is >> s)
	{
		switch (flag)
		{
			case 0:    //日期
			{
			    char *cha = (char*)s.data();
			    sscanf(cha, "%d-%d-%d", &tmp_data.year, &tmp_data.month, &tmp_data.day);
				flag++;
				break;
			}
		}
	}
	return tmp_data;
}
//读取input
Flaln ReadInput(const string flavor)
	{
	Flaln fla;
	istringstream is(flavor);
	string s;
	int flag = 0;
	while (is >> s)
		{
		switch (flag)
			{
			case 0:    //存储类型
				{
				fla.type = s;
				flag++;
				break;
				}
			case 1:    //存储CPU
				{
				fla.par[0] = atoi(s.c_str());
				flag++;
				break;
				}
			default:   //存储内存
				{
				fla.par[1] = atoi(s.c_str())/1024;
				break;
				}
			}
		}
	return fla;
	}

//匹配虚拟机种类
int match(const string fla, map<string, int> flavor_type)
	{
	int match_num;
	map<string, int>::iterator it;
	it = flavor_type.find(fla);
	if (it != flavor_type.end())
		match_num = it->second;
	else
		match_num = -1;                    //未匹配成功
	return match_num;
	}

//转化时间
time_t convert(Data data)
	{
	tm info = {0};
	info.tm_year = data.year - 1900;
	info.tm_mon = data.month - 1;
	info.tm_mday = data.day;
	return mktime(&info);
	}

//计算时间间隔
int CalculateInterval(Data data_this, Data data_up)
	{
	int this_data= (int)convert(data_this);
	int up_data = (int)convert(data_up);
	int interval = (this_data - up_data)/24/3600;
	return interval;
	}

/*************************************** WAN    *******************************************/
/******************************    预测算法所用子函数 放置区开始   ************************/
// 线性回归
#ifdef _LINEREG
void LineReg(double * para,vector<int> favorNum, int days )
{
    //double d1, d2, d3;
	double sumx,sumy,sumxx,sumyy,sumxy;
	//double mx,my,mxx,myy,mxy;
    int i,n,* x  = NULL,* y  = NULL;                                                              
	n = days;
	x = (int *)malloc(sizeof(int)*days);
	y = (int *)malloc(sizeof(int)*days);
	for( i = 0;i < days;i++)
	{
		x[i] = i+1;                                                           //默认第一天 时间变量为  1
		y[i] = favorNum[i];
	}

    // 变量的初始化
    sumx=sumy=sumxx=sumyy=sumxy=0.0;
	//d1 = d2 = d3 =0;
    // 计算x、y的平均值
    for (i = 0; i < n; i++) {
        sumx += x[i];
        sumy += y[i];
    }
    //mx = sumx / n;
    //my = sumy / n;
    //printf("\nmx=%f my=%f\n",mx,my);
    // 计算x、y平和x*y的平均值
    for (i = 0; i < n; i++) {
        sumxx += x[i]*x[i];
        sumyy += y[i]*y[i];
        sumxy += x[i]*y[i];
    }
    //mxx = sumxx / n;
    //myy = sumyy / n;
    //mxy = sumxy / n;
    //printf("mxx=%f myy=%f mxy=%f\n",mxx,myy,mxy);


    //
    para[0]=(n*sumxy-sumx*sumy)/(n*sumxx-sumx*sumx);
    para[1]=(sumxx*sumy-sumx*sumxy)/(n*sumxx-sumx*sumx);

   //printf("回归方程参数\tk=%f b=%f\n",para[0],para[1]);
 //   // 计算相关系数的数据组成部分
 //   for (i = 0; i < n; i++) {
 //       d1 += (x[i] - mx) * (y[i] - my);
 //       d2 += (x[i] - mx) * (x[i] - mx);
 //       d3 += (y[i] - my) * (y[i] - my);
 //   }
 //    
 //   double r = d1 / sqrt(d2 * d3);

 //   printf("相关系数r=%f\n",r);
 //
 //   double *yy=(double*)malloc(sizeof(double)*n);
 //   double sumerrorsquare=0,error;
 //   for(i=0;i<n;i++) {
 //       yy[i]=para[0]*x[i]+para[1];
 //       sumerrorsquare+=(yy[i]-y[i])*(yy[i]-y[i]);
 //   }
 //   error=sqrt(sumerrorsquare/(n-1));
 //   printf("标准偏差s(y)=%f\n",error);

	free(x);
	free(y);
	x = NULL;/*请加上这句*/
	y = NULL;/*请加上这句*/
}

#endif
/******************************    预测算法所用子函数 放置区结束  ************************/




/*************************************** MEI  *********************************************/
/******************************    放置算法所用子函数 放置区开始   ************************/

//该一种放完了，需要判断该服务器剩余空间能否再放下其他种类的虚拟机，如果不可以，就flag = 0
int JudgeRest(const Server server, const vector<Flaln> InputFlavor, int InputNum)
{
	int flag = 0;   //先设为不可以，根据后续判断是否可以
	for (int i = 0; i < InputNum; i++)
		if (InputFlavor[i].rest != 0 && InputFlavor[i].SingleVmFlag != 0)   //检查该种 ”虚拟机是否放置完“以及“是否可以在物理服务器上放置”
		{
			if ((server.par[0] >= InputFlavor[i].par[0]) && ((server.par[1] >= InputFlavor[i].par[1])))
			{
				flag = 1;
				break;    //一旦判断有一个可以，就说明剩余空间确实可以放置其他的虚拟机，退出循环
			}
		}
	return flag;
}

//将预测的五种虚拟机的动态数组传进去，选出需要放置的虚拟机种类。形参i如果是0优化CPU，如果是1优化内存
int SelectFlavorToSet(vector<Flaln> InputFlavor, int i, int InputNum)
{
	int fn = 0;
	int size = 0;
	vector<int> a;   //存储还没分配完的虚拟机的类型标号，后续就是在这里面筛选
	for (int j = 0; j < InputNum; j++)    //不能把上种虚拟机进入选择范围内
	{
		if (InputFlavor[j].rest != 0 && InputFlavor[j].SingleVmFlag != 0 )
			a.push_back(j);
	}
	size = a.size();
	for (int k = 1; k < size; k++)
	{
		if (InputFlavor[a[k]].par[i] > InputFlavor[a[k-1]].par[i])
		{
			fn = a[k];
		}
		else if (InputFlavor[a[k]].par[i] < InputFlavor[a[k-1]].par[i])
		{
			fn = a[k-1];
		}
		else
		{
			fn = InputFlavor[a[k]].par[1-i] > InputFlavor[a[k -1]].par[1-i] ? a[k] : a[k-1];
		}
	}
	return fn;
}

//判断是否都放置完了，是返回0；否返回1
int Judge(const vector<Flaln> InputFlavor, int InputNum)
{
	int flag = 1;
	int num = 0;
	for (int i = 0; i < InputNum; i++)
		if (InputFlavor[i].rest == 0)
			num++;
	if (num == InputNum)  //当每种虚拟机的剩余预测数量都为0，即全部放置完成
		flag = 0;
	return flag;
}
/***************************************放置算法所用子函数 放置区结束***********************************************/



//你要完成的功能总入口
//info---input.txt     data---TrainData.txt   data_num---TrainData num
void predict_server(char * info[MAX_INFO_NUM], char * data[MAX_DATA_NUM], int data_num, char * filename)
{
	/************************************************************************/
	/* 基本数据读取功能  Mei*/
	/************************************************************************/
	int InputNum = atoi(*(info + 2));    //需要预测的虚拟机种类数量
	vector<Flaln> InputFlavor;
	InputFlavor.resize(InputNum);

	map<string, int> flavor_type;
	for (int i = 3; i < InputNum + 3; i++)
	{
	    string tmp(info[i]);
		InputFlavor[i - 3] = ReadInput(tmp);   //读取信息到Flavor结构体数组
		flavor_type.insert(pair<string, int>(InputFlavor[i - 3].type, i - 3));   //将所有类型放进一个map里面
	}
	
	int physics_par[2];   //物理服务器参数数组
	string tmp_0(info[0]);
	ReadPhysicsPar(tmp_0, physics_par);

	int par;  //待优化的资源类型   par=0：CPU  par=1：内存
	string tmp_op(info[4+InputNum]);
	par = ReadTypeToOptimize(tmp_op);

	Data predict_data[2];     //predict_data[0]：首天   predict_data[1]：末天
	int predict_interval;     //预测的间隔天数,     
	int preStart_interval;     //预测第一天与历史最后一天的 间隔天数
	string tmp_pd_0(info[6+InputNum]);
	string tmp_pd_1(info[7+InputNum]);
	predict_data[0] = ReadFlagDay(tmp_pd_0);
	predict_data[1] = ReadFlagDay(tmp_pd_1);
	predict_interval = CalculateInterval(predict_data[1], predict_data[0]);     //从某天零点到某天零点，所以不需加 1

	/************************************************************************/
	/*筛选整理数据算法 Mei */
	/************************************************************************/
	//读取第一天的日期
	string train_data_0(data[0]);
	FlaTD td_0 = ReadSingleTrainData(train_data_0);

	//读取最后一天日期
	string train_data_end(data[data_num - 1]);
	FlaTD td_end = ReadSingleTrainData(train_data_end);

	//计算总天数并对每种虚拟机的num的大小设置，同时初始化，初始化结果为0
	int total_days = CalculateInterval(td_end.data, td_0.data) + 1;   //计算历史总天数   从1.1到2.19，共31+19=50天
	for (int i = 0; i < InputNum; i++)
	{
        InputFlavor[i].num.resize(total_days);
		InputFlavor[i].total = 0;    //先将预测时间段该种虚拟机访问数量的总和置为0，为后续求和做准备
	}

	int day_flag = 0;   //定义第几天   //说明：假设day_flag为0，则代表第一天
	Data data_this;    //设置本条信息日期
	Data data_up = td_0.data;   //设置上条信息
	//逐行筛选TrainData信息
	for (int i = 0; i < data_num; i++)
	{
		string train_data_this(data[i]);  //读取本条信息
		FlaTD td_this = ReadSingleTrainData(train_data_this);
		data_this = td_this.data;

		int interval = CalculateInterval(data_this, data_up);   //计算天数差
		day_flag+= interval;     //计天数
		int match_num = match(td_this.type, flavor_type);

		if (match_num != -1)    //匹配成功则在历史访问记录上加1
			InputFlavor[match_num].num[day_flag]++;   //匹配成功

		data_up = data_this;   //上面的时间差用完了就将本条信息置为上一条
	}

	/************************************************************************/
	/*预测算法  Wan*/
	//int predict_interval;  预测天数
	/************************************************************************/
		//预测算法
	/*************** WAN  ***********************/
	//线性回归代码 
	#ifdef _LINEREG

	double * PredictNum = NULL;                                          
	PredictNum = (double *)malloc(sizeof(double)*(predict_interval+1));      //某规格虚拟机在预测期每天数量,基于统计模型，所以可能为小数 

	preStart_interval = CalculateInterval(predict_data[0], td_end.data);  //预测第一天与历史最后一天的 间隔天数

//printf("\n\t\t预测虚拟机各规格数量\n类型\t数量\n");
	for (int i = 0; i < InputNum; i++)
	{
		PredictNum[predict_interval] = 0;  

		LineReg(LinePara,InputFlavor[i].num,total_days);
		for(int m =0;m < predict_interval;m++)
		{
		  PredictNum[m] = double(LinePara[0]*(total_days+preStart_interval+i)+LinePara[1]);      //默认第一天 时间变量为  1
		                                                                                         //预测第一天时间变量为 total_days+preStart_interval+i
		  PredictNum[predict_interval]  += PredictNum[m];                                        //将当前规格虚拟机每天预测的数量累加起来
		}


		InputFlavor[i].total = int(PredictNum[predict_interval])+1;             //将预测某种规格虚拟机的数据总和写入，并转化为int型，不足1补足1
		 if(InputFlavor[i].total < 0)
			 InputFlavor[i].total  =0;
		InputFlavor[i].rest = InputFlavor[i].total;                     //将某种规格虚拟机的放置后剩余量 填满，因放置还未进行。
		//cout << InputFlavor[i].type;                                    //将各种规格的虚拟机预测数量打印出来
		//printf("\t%d\n",InputFlavor[i].total);                                   
	}
	#endif
	/*******************************************/



	/************************************************************************/
	/*放置算法  Mei*/
	//在放置之前，把InputFlavor[i].total和InputFlavor[i].rest算出来，开始时total和rest相等
	//int par;   优化放置资源类型  par=0：CPU；par=1：内存
	//int physics_par[2];   物理服务器参数数组   physics_par[0]：CPU ；physics_par[1]：内存
	/************************************************************************/
	//建立物理服务器参数
	Server server;
	server.par[0] = physics_par[0];
	server.par[1] = physics_par[1];

	int OptimizeFlag = par;   //设置需要优化的资源标志：OptimizeFlag=0，即优化CPU；OptimizeFlag=1，即优化memory；则1-i即为需要考虑的不超的另外一项资源

	vector<Server> ser;   //设置一个服务器动态数组
	ser.push_back(server);  //首先放一个物理服务器   最后只需要ser.size()就可以知道需要设置多少个服务器了

	for(int i =0;i<  InputNum;i++)         //初始化 每种虚拟机在单台服务器都可放置
		InputFlavor[i].SingleVmFlag = 1;   

	int judge_flag = Judge(InputFlavor, InputNum);  /*是否都放置完了，这里需要写一个函数判断一下*/  //第一次judge_flag应该是1，可以放置
	int ToSerNum = 0;  //设置需要配置的服务器，ToSerNum = 0即第1个服务器
	int fn = 0;        //当前放置优先级最高的虚拟机 种类
	//放置算法核心部分
	while (judge_flag)    //当所有虚拟机配置完后，每种的剩余数量rest均为0，即为所有的配置完成
	{
		int flag = 1;  //设置能否配置的标志位，因为是还未配置的虚拟机，所以一开始是可以配置的
		ser[ToSerNum].flavor.resize(InputNum);  //将当前服务器的放置的各规格虚拟机数量初始化为0
		while (flag)
		{
			//选出需要放置的虚拟机种类
			fn = SelectFlavorToSet(InputFlavor, OptimizeFlag, InputNum);   //将预测的五种虚拟机的动态数组传进去（实际上返回的是该种在动态数组中的下标位置）

			//开始放置                                    //在新放一个之前先判断如果再加入一个是否会超内存
			for (int i = 0; i < InputFlavor[fn].rest; i++)
			{
				if (InputFlavor[fn].par[OptimizeFlag] <= ser[ToSerNum].par[OptimizeFlag] && 
					InputFlavor[fn].par[1-OptimizeFlag] <= ser[ToSerNum].par[1-OptimizeFlag])
				{
					ser[ToSerNum].flavor[fn]++;   //在该种服务器下将flavor[fn]这种虚拟机的配置数量加1
					InputFlavor[fn].rest--;  //上面的服务器加1，则该种虚拟机资源减1

					ser[ToSerNum].par[OptimizeFlag] -= InputFlavor[fn].par[OptimizeFlag];     //物理服务器CPU结算
					ser[ToSerNum].par[1-OptimizeFlag] -= InputFlavor[fn].par[1-OptimizeFlag];  //物理服务器内存结算
				}
				else
				{
					InputFlavor[fn].SingleVmFlag = 0;   //标志该虚拟机在该服务器上不能再放置
					break;   //内存没超，但服务器剩余的CPU数已经不能再放这种了虚拟机了，就跳出循环
				}
			}

			//进入到下面这个if的情况：1)该虚拟机已经放置完  2)该虚拟机已不能再该台服务器上放置
			if (!JudgeRest(ser[ToSerNum], InputFlavor, InputNum))   //需要判断该服务器剩余空间能否再放下其他种类的虚拟机，如果不可以，就flag = 0
				flag = 0;
		}

		if (Judge(InputFlavor, InputNum))  //判断一下，是不是所有虚拟机都配置完了，如果不是，那就新开一台物理服务器  //选择cpu最小，memory最小的
		{
			ser.push_back(server);   //新开一台物理服务器
			for(int i = 0; i< InputNum;i++)
				InputFlavor[i].SingleVmFlag = 1;            //在新的服务器上更新每种虚拟机放置开关，保证每种虚拟机在单台服务器都可放置
			ToSerNum++;  //为第二次的设置做准备
		}
		else
			judge_flag = 0;   //全部放置完了就置为0
	}

	/************************************************************************/
	/* 最后的格式输出  Mei*/
	/************************************************************************/

	// 需要输出的内容




	string Stemp;
	/*char c[1000];*/
	int size2 = 0,InSum = 0;
	const char * result_file = NULL;
	for(int i = 0;i < InputNum;i++)
		InSum += InputFlavor[i].total;
	Stemp= to_string (InSum);
	Stemp +='\n';
	for(int i=0;i<InputNum;i++)
	{
		Stemp += InputFlavor[i].type;
		Stemp +=' ';
		Stemp += to_string (InputFlavor[i].total);
		Stemp +='\n';
	}
	Stemp +='\n';

	size2 = ser.size();
	Stemp += to_string (size2);
	Stemp +='\n';
	for(int i=0;i<size2;i++)
	{
		Stemp += to_string (i+1);                         //第一台服务器  

		for(int j=0;j<InputNum;j++)
		{
          if(ser[i].flavor[j] != 0)
		  {
			Stemp += ' ';
			Stemp += InputFlavor[j].type;               //放置虚拟机的类型
			Stemp += ' ';                               
			Stemp += to_string (ser[i].flavor[j]);                  //放置当前类型虚拟机的数量
		  }
		}
		Stemp +='\n';
	}
	//len =Stemp.length();
	//result_file = (char *)malloc((len)*sizeof(char));
 //   Stemp.copy(result_file,len,0);
	 result_file = Stemp.c_str();


	// 直接调用输出文件的方法输出到指定文件中(ps请注意格式的正确性，如果有解，第一行只有一个数据；第二行为空；第三行开始才是具体的数据，数据之间用一个空格分隔开)
	write_result(result_file, filename);

	//while(*result_file != 0)
	//{
	//printf("%d\n",*result_file);
	//result_file++;
	//}

	#ifdef _LINEREG
	free(PredictNum);
	PredictNum = NULL;
	#endif
	//free(result_file);
	//result_file = NULL;


	}
