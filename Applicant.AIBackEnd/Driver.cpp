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

// 5 15 test_data.csv test_lbl.csv out 500 2 1.0 0.1
// 1 15 test_data.csv test_lbl.csv out 500 1 1.0 0.1
// out.txt test_data.csv

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
			vector<Eigen::SparseMatrix<double>> run_data;
			int numApplicants = 0;
			
			load_data(this->run_data_file,
					  numApplicants,
					  run_data);
			
			this->data = run_data;
			this->running_data_size = numApplicants;
		}
		else {
			vector<Eigen::SparseMatrix<double>> train_data, train_lbl;
			vector<Eigen::SparseMatrix<double>> test_data, test_lbl;
			int numApplicants = 0;
			load_data(this->train_data_file,
					  this->train_label_file,
					  numApplicants, train_data, train_lbl);
			this->training_data_size = numApplicants;
			load_data(this->test_data_file,
					  this->test_label_file,
					  numApplicants, test_data, test_lbl);
			this->testing_data_size = numApplicants;
			for (int i = 0; i < this->testing_data_size; ++i) {
				train_data[i].makeCompressed();
				train_lbl[i].makeCompressed();
				test_data[i].makeCompressed();
				test_lbl[i].makeCompressed();
				this->training.emplace_back(make_pair(move(train_data[i]), move(train_lbl[i])));
				this->testing.emplace_back(make_pair(move(test_data[i]), move(test_lbl[i])));
			}
			test_data.clear();
			test_lbl.clear();

			for (int i = testing_data_size; i < training_data_size; ++i) {
				train_data[i].makeCompressed();
				train_lbl[i].makeCompressed();
				this->training.emplace_back(make_pair(move(train_data[i]), move(train_lbl[i])));
			}
			train_data.clear();
			train_lbl.clear();
		}
	}

	void run() {
		this->input_layer_size = 0;
		this->input_layer_size = 0;
		vector<int> layers = { this->input_layer_size, this->hidden_layer_size, 2 };
		
		CrossEntropy cost;
		Classify ot;
		
		Network<CrossEntropy, Classify> net(layers, cost, ot);
		
		net.input(this->saved_net_file);
		
		for (unsigned i = 0; i < this->data.size(); ++i) {
			Eigen::MatrixXd result = net.feedforward_run(this->data[i]);
			cout << result(0,0);
		}
		
	}

	void train() {
		vector<int> layers;
		layers.push_back(this->input_layer_size);
		layers.push_back(this->hidden_layer_size);
		layers.push_back(2);
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
	double learning_rate;
	double lambda;
	bool is_trained;
};

int main(int argc, char * argv[]) {
	
	Data data(argc, argv);

	data.load();
	if (data.is_training()) { data.train(); }
	else { data.run(); }
	return 0;
}
