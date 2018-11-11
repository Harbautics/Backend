#include <iostream>
#include "Network.h"
#include "Load_data.h"

#define TRAIN_SIZE 1000
#define TEST_SIZE 100

//#define IMG_SIZE 784
//#define LBL_SIZE 10

//#define DATA_SIZE 18
//#define LBL_SIZE 2

/*
RUN:
./network [data | file] [saved network | file]
TRAIN:
./network [input layer size | int] \
		  [hidden layer size | int] \
		  [training_data_file | string] \
		  [training_label_file | string]
	      [output file | string] \
		  [epochs | int] \
		  [mini batch size | int] \
		  [eta | double] \
		  [lambda | double]
*/

using namespace std;

class Data {
public:
	Data(int argc, char * argv[]) {
		if (argc == 3) {
			this->saved_net_file = argv[1];
			this->run_data_file = argv[2];
			this->is_trained = true;
		}
		else if (argc == 10) {
			this->input_layer_size = atoi(argv[1]);
			this->hidden_layer_size = atoi(argv[2]);
			this->train_data_file = argv[3];
			this->train_label_file = argv[4];
			this->outfile = argv[5];
			this->epochs = atoi(argv[6]);
			this->mini_batch_size = atoi(argv[7]);
			this->learning_rate = atof(argv[8]);
			this->lambda = atof(argv[9]);
			this->is_trained = false;
		}
	}

	void load() {
		if (this->is_trained) {
			//vector<Eigen::SparseMatrix<double>> run_data;
			int numApplicants = 0;
			load_data(this->run_data_file,
					  numApplicants,
					  /*this->data_size,*/
					  this->data);
			this->running_data_size = numApplicants;
		}
		else {
			vector<Eigen::SparseMatrix<double>> train_data, train_lbl;
			vector<Eigen::SparseMatrix<double>> test_data, test_lbl;
			int numApplicants = 0;
			load_data(this->train_data_file,
					  this->train_label_file,
					  numApplicants, /*this->data_size,*/ train_data, train_lbl);
			this->training_data_size = numApplicants;
			load_data(this->test_data_file,
					  this->test_label_file,
					  numApplicants, /*this->data_size,*/ test_data, test_lbl);
			this->testing_data_size = numApplicants;
			for (unsigned i = 0; i < this->testing_data_size; ++i) {
				train_data[i].makeCompressed();
				train_lbl[i].makeCompressed();
				test_data[i].makeCompressed();
				test_lbl[i].makeCompressed();
				this->training.emplace_back(make_pair(move(train_data[i]), move(train_lbl[i])));
				this->testing.emplace_back(make_pair(move(test_data[i]), move(test_lbl[i])));
			}
			test_data.clear();
			test_lbl.clear();

			for (unsigned i = testing_data_size; i < training_data_size; ++i) {
				train_data[i].makeCompressed();
				train_lbl[i].makeCompressed();
				this->training.emplace_back(make_pair(move(train_data[i]), move(train_lbl[i])));
			}
			train_data.clear();
			train_lbl.clear();
		}
	}

	void run() {
		vector<int> layers = { this->input_layer_size, this->hidden_layer_size, 1 };
		CrossEntropy cost;
		Classify ot;
		Network<CrossEntropy, Classify> net(layers, cost, ot);
		net.input(this->saved_net_file);
		for (unsigned i = 0; i < this->data.size(); ++i) {
			Eigen::MatrixXd result = net.feedforward(this->data[i]);
			cout << result << endl;
		}
	}

	void train() {
		vector<int> layers = { this->input_layer_size, this->hidden_layer_size, 1 };
		CrossEntropy cost;
		Classify ot;
		Network<CrossEntropy, Classify> net(layers, cost, ot);
		net.SGD(this->training,
			this->epochs,
			this->mini_batch_size,
			this->learning_rate,
			this->lambda);
				//this->testing, 
				//true, true, true, true);
		net.output(this->outfile);
	}

	bool is_training() {
		return !this->is_trained;
	}

	//void set_all_data(vector<Eigen::SparseMatrix<double>> &data, vector<Eigen::SparseMatrix<double>> &labels) {
	//	this->
	//}

private:
	vector<inout> training;
	vector<inout> testing;
	vector<Eigen::SparseMatrix<double>> data;
	string train_data_file;
	string train_label_file;
	string test_data_file;
	string test_label_file;
	string outfile;
	string saved_net_file;
	string run_data_file; 
	int input_layer_size;
	int hidden_layer_size;
	int training_data_size;
	int testing_data_size;
	int running_data_size;
	int epochs;
	int mini_batch_size;
	int learning_rate;
	int lambda;
	bool is_trained;
};

int console_call(int argc, char * argv[], Network<CrossEntropy, Classify> * net);

int main(int argc, char * argv[]) {
	/*vector<Eigen::SparseMatrix<double>> train_data, train_lbl;
	vector<Eigen::SparseMatrix<double>> test_data, test_lbl;*/
	/*vector<inout> training;
	vector<inout> testing;*/

	Data data(argc, argv);

	/*load_data(train_data_file,
			  train_label_file,
			  TRAIN_SIZE, DATA_SIZE, train_data, train_lbl);
	load_data(test_data_file,
			  test_label_file,
			  TEST_SIZE, DATA_SIZE, test_data, test_lbl);*/

	/*pair<Eigen::MatrixXd, Eigen::MatrixXd> train;
	pair<Eigen::MatrixXd, Eigen::MatrixXd> test;
	for (unsigned i = 0; i < TEST_SIZE; ++i) {
		train_data[i].makeCompressed();
		train_lbl[i].makeCompressed();
		test_data[i].makeCompressed();
		test_lbl[i].makeCompressed();
		//cout << train_lbl[i] << endl;
		train = make_pair(move(train_data[i]), move(train_lbl[i]));
		test = make_pair(move(test_data[i]), move(test_lbl[i]));
		training.emplace_back(move(train));
		testing.emplace_back(move(test));
	}
	test_data.clear();
	test_lbl.clear();*/
	//cout << endl;
	/*for (unsigned i = TEST_SIZE; i < TRAIN_SIZE; ++i) {
		//train = make_pair(move(train_data[i]), move(train_lbl[i]));
		training.emplace_back(make_pair(move(train_data[i]), move(train_lbl[i])));
	}*/
	cout << "Beginning training\n";
	data.load();
	if (data.is_training()) { data.train(); }
	else { data.run(); }
	//train_data.clear();
	//string outfile = "trainedNet.txt";
	//train_lbl.clear();
	/*vector<int> layers = { 784,30,10 };
	CrossEntropy cost;
	Classify ot;
	Network<CrossEntropy, Classify> net(layers, cost, ot);
	net.SGD(training, 30, 100, 0.1, 1.0, testing, true, true, true, true);
	net.output(outfile);*/
	cout << endl;
	return 0;
}

/*int console_call(int argc, char * argv[], Network<CrossEntropy, Classify> * net) {
	if (argc == 1) {
		string data = argv[1];
		net->input(data);

	}
	else if (argc == 8) {

	}
	return 0;
}*/