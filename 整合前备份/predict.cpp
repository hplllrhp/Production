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
//�ع���� 
#ifdef _LINEREG
#define   LParaNum    2                         //�ع��������
#endif
/*******************************************/

using namespace std;



//���ڽṹ��
struct Data {
	int year;
	int month;
	int day;
	};

//input������ṹ��
struct Flaln
	{
	string type;     //���������
	int par[2];    //par[0]:cpu   par[1]:memory
	vector<int> num;  //������̬���飬InputFlavor[i].num[j]:��i��������ڵ�j���ʹ������
	int total;   //Ԥ��ʱ��θ�������������������ܺ�
	int rest;    //���ú�ʣ��ĸ������������
	int SingleVmFlag;   //�ڵ�̨�������Ϸ�����ɿ���   Ϊ0ʱ�������ڸ÷������Ϸ���  Ϊ1ʱ���ڸ÷������Ϸ���
	};

//TrainData��Ϣ�ṹ��
struct FlaTD {
	string type;
	Data data;
	};

//����input��������������Ĳ���   //����Ҳ���Լ򻯴���
struct Server
{
	int par[2];  //par[0]:CPU����   par[1]:�ڴ��С
	vector<int> flavor;  //flavor[0]��ʾҪ�ŵĵ�1���������̨�����������±�ֱ�Ӵ�������������࣬�����Կ���flavor.resize(InputNum)
};


/*************** WAN  ***********************/
//���Իع鷽�̲��� �洢����
#ifdef _LINEREG
double LinePara[LParaNum];                       //�ع��ò���
#endif
/*******************************************/



//��ȡ����TrainData
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
			case 0:    //�����û���
				{
				flag++;
				break;
				}
			case 1:    //�洢flavor����
				{
				fla.type = s;
				flag++;
				break;
				}
			case 2:   //�洢����
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

//��ȡ���������CPU���ڴ�
void ReadPhysicsPar(string tmp, int par[])
{
	istringstream is(tmp);
	string s;
	int flag = 0;
	while (is >> s)
	{
	    switch (flag)
		{
		    case 0:    //�洢CPU
			{
			    par[0] = atoi(s.c_str());
			    flag++;
			    break;
			}
		    case 1:    //�洢�ڴ�
			{
			    par[1] = atoi(s.c_str());
			    flag++;
			    break;
			}
		}
	}
}

//��ȡ���Ż�����Դ����
int ReadTypeToOptimize(string tmp)
{
    int flag = 1;
    if (tmp == "CPU")
		flag = 0;
	return flag;
}

//��ȡ��Ԥ������ʱ���
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
			case 0:    //����
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
//��ȡinput
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
			case 0:    //�洢����
				{
				fla.type = s;
				flag++;
				break;
				}
			case 1:    //�洢CPU
				{
				fla.par[0] = atoi(s.c_str());
				flag++;
				break;
				}
			default:   //�洢�ڴ�
				{
				fla.par[1] = atoi(s.c_str())/1024;
				break;
				}
			}
		}
	return fla;
	}

//ƥ�����������
int match(const string fla, map<string, int> flavor_type)
	{
	int match_num;
	map<string, int>::iterator it;
	it = flavor_type.find(fla);
	if (it != flavor_type.end())
		match_num = it->second;
	else
		match_num = -1;                    //δƥ��ɹ�
	return match_num;
	}

//ת��ʱ��
time_t convert(Data data)
	{
	tm info = {0};
	info.tm_year = data.year - 1900;
	info.tm_mon = data.month - 1;
	info.tm_mday = data.day;
	return mktime(&info);
	}

//����ʱ����
int CalculateInterval(Data data_this, Data data_up)
	{
	int this_data= (int)convert(data_this);
	int up_data = (int)convert(data_up);
	int interval = (this_data - up_data)/24/3600;
	return interval;
	}

/*************************************** WAN    *******************************************/
/******************************    Ԥ���㷨�����Ӻ��� ��������ʼ   ************************/
// ���Իع�
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
		x[i] = i+1;                                                           //Ĭ�ϵ�һ�� ʱ�����Ϊ  1
		y[i] = favorNum[i];
	}

    // �����ĳ�ʼ��
    sumx=sumy=sumxx=sumyy=sumxy=0.0;
	//d1 = d2 = d3 =0;
    // ����x��y��ƽ��ֵ
    for (i = 0; i < n; i++) {
        sumx += x[i];
        sumy += y[i];
    }
    //mx = sumx / n;
    //my = sumy / n;
    //printf("\nmx=%f my=%f\n",mx,my);
    // ����x��yƽ��x*y��ƽ��ֵ
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

   //printf("�ع鷽�̲���\tk=%f b=%f\n",para[0],para[1]);
 //   // �������ϵ����������ɲ���
 //   for (i = 0; i < n; i++) {
 //       d1 += (x[i] - mx) * (y[i] - my);
 //       d2 += (x[i] - mx) * (x[i] - mx);
 //       d3 += (y[i] - my) * (y[i] - my);
 //   }
 //    
 //   double r = d1 / sqrt(d2 * d3);

 //   printf("���ϵ��r=%f\n",r);
 //
 //   double *yy=(double*)malloc(sizeof(double)*n);
 //   double sumerrorsquare=0,error;
 //   for(i=0;i<n;i++) {
 //       yy[i]=para[0]*x[i]+para[1];
 //       sumerrorsquare+=(yy[i]-y[i])*(yy[i]-y[i]);
 //   }
 //   error=sqrt(sumerrorsquare/(n-1));
 //   printf("��׼ƫ��s(y)=%f\n",error);

	free(x);
	free(y);
	x = NULL;/*��������*/
	y = NULL;/*��������*/
}

#endif
/******************************    Ԥ���㷨�����Ӻ��� ����������  ************************/




/*************************************** MEI  *********************************************/
/******************************    �����㷨�����Ӻ��� ��������ʼ   ************************/

//��һ�ַ����ˣ���Ҫ�жϸ÷�����ʣ��ռ��ܷ��ٷ���������������������������ԣ���flag = 0
int JudgeRest(const Server server, const vector<Flaln> InputFlavor, int InputNum)
{
	int flag = 0;   //����Ϊ�����ԣ����ݺ����ж��Ƿ����
	for (int i = 0; i < InputNum; i++)
		if (InputFlavor[i].rest != 0 && InputFlavor[i].SingleVmFlag != 0)   //������ ��������Ƿ�����ꡰ�Լ����Ƿ����������������Ϸ��á�
		{
			if ((server.par[0] >= InputFlavor[i].par[0]) && ((server.par[1] >= InputFlavor[i].par[1])))
			{
				flag = 1;
				break;    //һ���ж���һ�����ԣ���˵��ʣ��ռ�ȷʵ���Է�����������������˳�ѭ��
			}
		}
	return flag;
}

//��Ԥ�������������Ķ�̬���鴫��ȥ��ѡ����Ҫ���õ���������ࡣ�β�i�����0�Ż�CPU�������1�Ż��ڴ�
int SelectFlavorToSet(vector<Flaln> InputFlavor, int i, int InputNum)
{
	int fn = 0;
	int size = 0;
	vector<int> a;   //�洢��û�����������������ͱ�ţ�����������������ɸѡ
	for (int j = 0; j < InputNum; j++)    //���ܰ��������������ѡ��Χ��
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

//�ж��Ƿ񶼷������ˣ��Ƿ���0���񷵻�1
int Judge(const vector<Flaln> InputFlavor, int InputNum)
{
	int flag = 1;
	int num = 0;
	for (int i = 0; i < InputNum; i++)
		if (InputFlavor[i].rest == 0)
			num++;
	if (num == InputNum)  //��ÿ���������ʣ��Ԥ��������Ϊ0����ȫ���������
		flag = 0;
	return flag;
}
/***************************************�����㷨�����Ӻ��� ����������***********************************************/



//��Ҫ��ɵĹ��������
//info---input.txt     data---TrainData.txt   data_num---TrainData num
void predict_server(char * info[MAX_INFO_NUM], char * data[MAX_DATA_NUM], int data_num, char * filename)
{
	/************************************************************************/
	/* �������ݶ�ȡ����  Mei*/
	/************************************************************************/
	int InputNum = atoi(*(info + 2));    //��ҪԤ����������������
	vector<Flaln> InputFlavor;
	InputFlavor.resize(InputNum);

	map<string, int> flavor_type;
	for (int i = 3; i < InputNum + 3; i++)
	{
	    string tmp(info[i]);
		InputFlavor[i - 3] = ReadInput(tmp);   //��ȡ��Ϣ��Flavor�ṹ������
		flavor_type.insert(pair<string, int>(InputFlavor[i - 3].type, i - 3));   //���������ͷŽ�һ��map����
	}
	
	int physics_par[2];   //�����������������
	string tmp_0(info[0]);
	ReadPhysicsPar(tmp_0, physics_par);

	int par;  //���Ż�����Դ����   par=0��CPU  par=1���ڴ�
	string tmp_op(info[4+InputNum]);
	par = ReadTypeToOptimize(tmp_op);

	Data predict_data[2];     //predict_data[0]������   predict_data[1]��ĩ��
	int predict_interval;     //Ԥ��ļ������,     
	int preStart_interval;     //Ԥ���һ������ʷ���һ��� �������
	string tmp_pd_0(info[6+InputNum]);
	string tmp_pd_1(info[7+InputNum]);
	predict_data[0] = ReadFlagDay(tmp_pd_0);
	predict_data[1] = ReadFlagDay(tmp_pd_1);
	predict_interval = CalculateInterval(predict_data[1], predict_data[0]);     //��ĳ����㵽ĳ����㣬���Բ���� 1

	/************************************************************************/
	/*ɸѡ���������㷨 Mei */
	/************************************************************************/
	//��ȡ��һ�������
	string train_data_0(data[0]);
	FlaTD td_0 = ReadSingleTrainData(train_data_0);

	//��ȡ���һ������
	string train_data_end(data[data_num - 1]);
	FlaTD td_end = ReadSingleTrainData(train_data_end);

	//��������������ÿ���������num�Ĵ�С���ã�ͬʱ��ʼ������ʼ�����Ϊ0
	int total_days = CalculateInterval(td_end.data, td_0.data) + 1;   //������ʷ������   ��1.1��2.19����31+19=50��
	for (int i = 0; i < InputNum; i++)
	{
        InputFlavor[i].num.resize(total_days);
		InputFlavor[i].total = 0;    //�Ƚ�Ԥ��ʱ��θ�������������������ܺ���Ϊ0��Ϊ���������׼��
	}

	int day_flag = 0;   //����ڼ���   //˵��������day_flagΪ0��������һ��
	Data data_this;    //���ñ�����Ϣ����
	Data data_up = td_0.data;   //����������Ϣ
	//����ɸѡTrainData��Ϣ
	for (int i = 0; i < data_num; i++)
	{
		string train_data_this(data[i]);  //��ȡ������Ϣ
		FlaTD td_this = ReadSingleTrainData(train_data_this);
		data_this = td_this.data;

		int interval = CalculateInterval(data_this, data_up);   //����������
		day_flag+= interval;     //������
		int match_num = match(td_this.type, flavor_type);

		if (match_num != -1)    //ƥ��ɹ�������ʷ���ʼ�¼�ϼ�1
			InputFlavor[match_num].num[day_flag]++;   //ƥ��ɹ�

		data_up = data_this;   //�����ʱ��������˾ͽ�������Ϣ��Ϊ��һ��
	}

	/************************************************************************/
	/*Ԥ���㷨  Wan*/
	//int predict_interval;  Ԥ������
	/************************************************************************/
		//Ԥ���㷨
	/*************** WAN  ***********************/
	//���Իع���� 
	#ifdef _LINEREG

	double * PredictNum = NULL;                                          
	PredictNum = (double *)malloc(sizeof(double)*(predict_interval+1));      //ĳ����������Ԥ����ÿ������,����ͳ��ģ�ͣ����Կ���ΪС�� 

	preStart_interval = CalculateInterval(predict_data[0], td_end.data);  //Ԥ���һ������ʷ���һ��� �������

//printf("\n\t\tԤ����������������\n����\t����\n");
	for (int i = 0; i < InputNum; i++)
	{
		PredictNum[predict_interval] = 0;  

		LineReg(LinePara,InputFlavor[i].num,total_days);
		for(int m =0;m < predict_interval;m++)
		{
		  PredictNum[m] = double(LinePara[0]*(total_days+preStart_interval+i)+LinePara[1]);      //Ĭ�ϵ�һ�� ʱ�����Ϊ  1
		                                                                                         //Ԥ���һ��ʱ�����Ϊ total_days+preStart_interval+i
		  PredictNum[predict_interval]  += PredictNum[m];                                        //����ǰ��������ÿ��Ԥ��������ۼ�����
		}


		InputFlavor[i].total = int(PredictNum[predict_interval])+1;             //��Ԥ��ĳ�ֹ��������������ܺ�д�룬��ת��Ϊint�ͣ�����1����1
		 if(InputFlavor[i].total < 0)
			 InputFlavor[i].total  =0;
		InputFlavor[i].rest = InputFlavor[i].total;                     //��ĳ�ֹ��������ķ��ú�ʣ���� ����������û�δ���С�
		//cout << InputFlavor[i].type;                                    //�����ֹ��������Ԥ��������ӡ����
		//printf("\t%d\n",InputFlavor[i].total);                                   
	}
	#endif
	/*******************************************/



	/************************************************************************/
	/*�����㷨  Mei*/
	//�ڷ���֮ǰ����InputFlavor[i].total��InputFlavor[i].rest���������ʼʱtotal��rest���
	//int par;   �Ż�������Դ����  par=0��CPU��par=1���ڴ�
	//int physics_par[2];   �����������������   physics_par[0]��CPU ��physics_par[1]���ڴ�
	/************************************************************************/
	//�����������������
	Server server;
	server.par[0] = physics_par[0];
	server.par[1] = physics_par[1];

	int OptimizeFlag = par;   //������Ҫ�Ż�����Դ��־��OptimizeFlag=0�����Ż�CPU��OptimizeFlag=1�����Ż�memory����1-i��Ϊ��Ҫ���ǵĲ���������һ����Դ

	vector<Server> ser;   //����һ����������̬����
	ser.push_back(server);  //���ȷ�һ�����������   ���ֻ��Ҫser.size()�Ϳ���֪����Ҫ���ö��ٸ���������

	for(int i =0;i<  InputNum;i++)         //��ʼ�� ÿ��������ڵ�̨���������ɷ���
		InputFlavor[i].SingleVmFlag = 1;   

	int judge_flag = Judge(InputFlavor, InputNum);  /*�Ƿ񶼷������ˣ�������Ҫдһ�������ж�һ��*/  //��һ��judge_flagӦ����1�����Է���
	int ToSerNum = 0;  //������Ҫ���õķ�������ToSerNum = 0����1��������
	int fn = 0;        //��ǰ�������ȼ���ߵ������ ����
	//�����㷨���Ĳ���
	while (judge_flag)    //������������������ÿ�ֵ�ʣ������rest��Ϊ0����Ϊ���е��������
	{
		int flag = 1;  //�����ܷ����õı�־λ����Ϊ�ǻ�δ���õ������������һ��ʼ�ǿ������õ�
		ser[ToSerNum].flavor.resize(InputNum);  //����ǰ�������ķ��õĸ���������������ʼ��Ϊ0
		while (flag)
		{
			//ѡ����Ҫ���õ����������
			fn = SelectFlavorToSet(InputFlavor, OptimizeFlag, InputNum);   //��Ԥ�������������Ķ�̬���鴫��ȥ��ʵ���Ϸ��ص��Ǹ����ڶ�̬�����е��±�λ�ã�

			//��ʼ����                                    //���·�һ��֮ǰ���ж�����ټ���һ���Ƿ�ᳬ�ڴ�
			for (int i = 0; i < InputFlavor[fn].rest; i++)
			{
				if (InputFlavor[fn].par[OptimizeFlag] <= ser[ToSerNum].par[OptimizeFlag] && 
					InputFlavor[fn].par[1-OptimizeFlag] <= ser[ToSerNum].par[1-OptimizeFlag])
				{
					ser[ToSerNum].flavor[fn]++;   //�ڸ��ַ������½�flavor[fn]���������������������1
					InputFlavor[fn].rest--;  //����ķ�������1��������������Դ��1

					ser[ToSerNum].par[OptimizeFlag] -= InputFlavor[fn].par[OptimizeFlag];     //���������CPU����
					ser[ToSerNum].par[1-OptimizeFlag] -= InputFlavor[fn].par[1-OptimizeFlag];  //����������ڴ����
				}
				else
				{
					InputFlavor[fn].SingleVmFlag = 0;   //��־��������ڸ÷������ϲ����ٷ���
					break;   //�ڴ�û������������ʣ���CPU���Ѿ������ٷ�������������ˣ�������ѭ��
				}
			}

			//���뵽�������if�������1)��������Ѿ�������  2)��������Ѳ����ٸ�̨�������Ϸ���
			if (!JudgeRest(ser[ToSerNum], InputFlavor, InputNum))   //��Ҫ�жϸ÷�����ʣ��ռ��ܷ��ٷ���������������������������ԣ���flag = 0
				flag = 0;
		}

		if (Judge(InputFlavor, InputNum))  //�ж�һ�£��ǲ���������������������ˣ�������ǣ��Ǿ��¿�һ̨���������  //ѡ��cpu��С��memory��С��
		{
			ser.push_back(server);   //�¿�һ̨���������
			for(int i = 0; i< InputNum;i++)
				InputFlavor[i].SingleVmFlag = 1;            //���µķ������ϸ���ÿ����������ÿ��أ���֤ÿ��������ڵ�̨���������ɷ���
			ToSerNum++;  //Ϊ�ڶ��ε�������׼��
		}
		else
			judge_flag = 0;   //ȫ���������˾���Ϊ0
	}

	/************************************************************************/
	/* ���ĸ�ʽ���  Mei*/
	/************************************************************************/

	// ��Ҫ���������




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
		Stemp += to_string (i+1);                         //��һ̨������  

		for(int j=0;j<InputNum;j++)
		{
          if(ser[i].flavor[j] != 0)
		  {
			Stemp += ' ';
			Stemp += InputFlavor[j].type;               //���������������
			Stemp += ' ';                               
			Stemp += to_string (ser[i].flavor[j]);                  //���õ�ǰ���������������
		  }
		}
		Stemp +='\n';
	}
	//len =Stemp.length();
	//result_file = (char *)malloc((len)*sizeof(char));
 //   Stemp.copy(result_file,len,0);
	 result_file = Stemp.c_str();


	// ֱ�ӵ�������ļ��ķ��������ָ���ļ���(ps��ע���ʽ����ȷ�ԣ�����н⣬��һ��ֻ��һ�����ݣ��ڶ���Ϊ�գ������п�ʼ���Ǿ�������ݣ�����֮����һ���ո�ָ���)
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
