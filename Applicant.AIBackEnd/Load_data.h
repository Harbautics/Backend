#ifndef LOAD_MNIST_H
#define LOAD_MNIST_H

//#define DATA_SIZE 784
#define LBL_SIZE 2

#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <Eigen/Sparse>
#include <Eigen/Dense>

using namespace std;
/*int ReverseInt(int i)
{
	unsigned char ch1, ch2, ch3, ch4;
	ch1 = i & 255;
	ch2 = (i >> 8) & 255;
	ch3 = (i >> 16) & 255;
	ch4 = (i >> 24) & 255;
	return((int)ch1 << 24) + ((int)ch2 << 16) + ((int)ch3 << 8) + ch4;
}*/

/*load_data(this->run_data_file,
				this->run_data_size,
				this->data_size,
				this->data);*/

void load_data(string dataFile, int &numApplicants, /*int dataSize,*/ vector<Eigen::SparseMatrix<double>> &data) {
	ifstream file(dataFile);
	string temp = "";
	//int numApplicants = 0;
	int numCategories = 0;
	getline(file, temp, ',');
	stringstream toint(temp);
	toint >> numApplicants;
	getline(file, temp, ',');
	toint.clear();
	toint.str(temp);
	toint >> numCategories;
	data.resize(numApplicants, Eigen::SparseVector<double>(numCategories));
	
	if (file.is_open()) {
		
		for (int i = 0; i<numApplicants; ++i)
		{
			for (int j = 0; j<numCategories; ++j)
			{
				string temp = "";
				getline(file, temp, ',');
				stringstream todouble(temp);
				double val = 0;
				todouble >> val;
				data[i].insert(j, 0) = val;
			}
		}
	}
	return;
}

void load_data(string dataFile, string lblFile, int &numApplicants, /*int DataOfAnImage,*/ 
			   vector<Eigen::SparseMatrix<double>> &data, vector<Eigen::SparseMatrix<double>> &lbl)
{
	ifstream file1(dataFile);
	string temp = "";
	//int numApplicants = 0;
	int numCategories = 0;
	getline(file1, temp, ',');
	stringstream toint(temp);
	toint >> numApplicants;
	getline(file1, temp, ',');
	toint.clear();
	toint.str(temp);
	toint >> numCategories;
	data.resize(numApplicants, Eigen::SparseVector<double>(numCategories));
	
	if (file1.is_open())
	{
		for (int i = 0; i<numApplicants; ++i)
		{
			for (int j = 0; j<numCategories; ++j)
			{
				string temp = "";
				getline(file1, temp, ',');
				stringstream todouble(temp);
				double val = 0.0;
				todouble >> val;
				data[i].insert(j, 0) = val;
			}
		}
	}


	lbl.resize(numApplicants, Eigen::SparseVector<double>(LBL_SIZE));
	ifstream file2(lblFile);
	if (file2.is_open())
	{
		/*string temp = "";
		int n_rows = 0;
		int n_cols = 0;
		getline(file2, temp, ',');
		stringstream toint(temp);
		toint >> n_rows;
		getline(file2, temp, ',');
		toint.clear();
		toint.str(temp);
		toint >> n_cols;*/
		//if (NumberOfNodes > number_of_nodes) { NumberOfNodes = number_of_nodes; }
		for (int i = 0; i < numApplicants; ++i)
		{
			std::string temp = "";
			getline(file2, temp, ',');
			std::stringstream toint(temp);
			int index = 0;
			toint >> index;
			//unsigned char temp = 0;
			//file2.read((char*)&temp, sizeof(temp));
			//double label = (double)temp;
			//int index = (int)temp;
			for (int j = 0; j < LBL_SIZE; ++j) {
				if (index == j) { 
					lbl[i].insert(j, 0) = 1.0; 
				}
				else { 
					lbl[i].insert(j, 0) = 0.0; 
				}
			}
		}
	}
}

#endif