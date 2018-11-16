#ifndef COST_H
#define COST_H

#include <cmath>
#include <iostream>
#include <cassert>
#include <vector>
#include <iostream>
//#include "matrix.h"

double norm(const Eigen::MatrixXd &vec);
double sigmoid(double z);
std::vector<double> sigmoid(const std::vector<double> &z);
Eigen::MatrixXd sigmoid(const Eigen::MatrixXd &z);
double sigmoid_prime(double z);

template <typename T>
std::vector<T> operator+(const std::vector<T>& v1, const std::vector<T>& v2) {
	assert(v1.size() == v2.size());
	std::vector<T> result(v1.size());
	for (unsigned i = 0; i < v1.size(); ++i) {
		result[i] = v1[i] + v2[i];
	}
	return result;
}

template <typename T>
std::vector<T> operator-(const std::vector<T>& v1, const std::vector<T>& v2) {
	assert(v1.size() == v2.size());
	std::vector<T> result(v1.size());
	for (unsigned i = 0; i < v1.size(); ++i) {
		result[i] = v1[i] - v2[i];
	}
	return result;
}

class CrossEntropy {
public:
	double fn(Eigen::MatrixXd a, const Eigen::MatrixXd &y) {
		assert(a.rows() == y.rows());
		double result = 0;
		for (int i = 0; i < a.rows(); ++i) {
			if (a(i, 0) == 0) {
				a(i, 0) = 0.00000000000001;
			}
			else if (1 - a(i, 0) == 0) {
				a(i, 0) = 0.99999999999999;
			}
			result += -y(i, 0) * std::log(a(i, 0)) - (1 - y(i, 0))*std::log(1 - a(i, 0));
		}
		return result;
	}

	Eigen::MatrixXd delta(const Eigen::MatrixXd &z, const Eigen::MatrixXd &a, const Eigen::MatrixXd &y) {
		assert(a.rows() == y.rows());
		assert(a.cols() == y.cols());
		//Eigen::MatrixXd result(a.rows(), a.cols());
		/*for (int i = 0; i < a.rows(); ++i) {
			for (int j = 0; j < a.cols(); ++j) {
				result(i, j) = a(i, j) - y(i, j);
			}
		}*/
		//result = a - y;
		return a - y;
	}
};

class Quadratic {
public:
	double fn(Eigen::MatrixXd a, const Eigen::MatrixXd &y) {
		assert(a.size() == y.size());
		double result = 0.0;
		/*for (int i = 0; i < a.rows(); ++i) {
			result += std::pow(y(i, 0) - a(i, 0), 2) / 2;
		}*/
		return 0.5*std::pow(norm(a - y), 2);
		//return result;
	}

	Eigen::MatrixXd delta(const Eigen::MatrixXd &z, Eigen::MatrixXd a, const Eigen::MatrixXd &y) {
		assert(a.size() == y.size());
		for (int i = 0; i < a.rows(); ++i) {
			for (int j = 0; j < a.cols(); j++) {
				a(i, j) = (a(i, j) - y(i, j)) * sigmoid_prime(z(i, j));
			}
		}
		return a;
	}
};

int argmax(std::vector<double> args) {
	double max_val = 0.0;
	int max_index = 0;
	for (unsigned i = 0; i < args.size(); ++i) {
		if (max_val < args[i]) {
			max_val = args[i];
			max_index = i;
		}
	}
	return max_index;
}

int argmax(Eigen::VectorXd args) {
	assert(args.cols() == 1);
	double max_val = 0.0;
	double val;
	int max_index = 0;
	for (int i = 0; i < args.rows(); ++i) {
		val = args(i, 0);
		if (max_val < args(i, 0)) {
			max_val = args(i, 0);
			max_index = i;
		}
	}

	return max_index;
}

double norm(const Eigen::MatrixXd &vec) {
	double result = 0;
	for (int i = 0; i < vec.rows(); ++i) {
		for (int j = 0; j < vec.cols(); ++j) {
			result += std::pow(vec(i, j), 2);
		}
	}
	return std::sqrt(result);
}

double sigmoid(double z) {
	return 1.0 / (1.0 + std::exp(0.0 - z));
}

std::vector<double> sigmoid(const std::vector<double> &z) {
	std::vector<double> result(z.size());
	for (unsigned i = 0; i < z.size(); ++i) {
		result[i] = sigmoid(z[i]);
	}
	return result;
}

Eigen::MatrixXd sigmoid(const Eigen::MatrixXd &z) {
	Eigen::MatrixXd result(z.rows(), z.cols());
	for (int i = 0; i < z.rows(); ++i) {
		for (int j = 0; j < z.cols(); ++j) {
			//std::cout << z(i, j) << std::endl;
			result(i, j) = 1.0 / (1.0 + std::exp(0.0 - z(i, j)));
			//std::cout << result(i, j) << std::endl;
		}
		//result[i] = sigmoid(z[i]);
	}
	return result;
	//return Eigen::MatrixXd::Ones(z.rows(), z.cols()).cwiseQuotient(Eigen::MatrixXd::Ones(z.rows(), z.cols()) + (Eigen::MatrixXd::Zero(z.rows(), z.cols()) - z).exp());
}

double sigmoid_prime(double z) {
	return sigmoid(z)*(1 - sigmoid(z));
}

std::vector<double> sigmoid_prime(const std::vector<double> &z) {
	std::vector<double> result(z.size());
	for (unsigned i = 0; i < z.size(); ++i) {
		result[i] = sigmoid_prime(z[i]);
	}
	return result;
}

Eigen::MatrixXd sigmoid_prime(const Eigen::MatrixXd &z) {
	Eigen::MatrixXd result(z.rows(), z.cols());
	/*for (int i = 0; i < z.rows(); ++i) {
		for (int j = 0; j < z.cols(); ++j) {
			result(i, j) = sigmoid(z(i, j))*(1 - sigmoid(z(i, j)));
		}
		//result[i] = sigmoid_prime(z[i]);
	}
	return result;*/
	return sigmoid(z).cwiseProduct(Eigen::MatrixXd::Ones(z.rows(), z.cols()) - sigmoid(z));
}

class Classify {
public:
	Eigen::MatrixXd outputFN(const Eigen::MatrixXd &z) {
		return sigmoid(z);
	}
};

class SoftMax {
public:
	Eigen::MatrixXd outputFN(const Eigen::MatrixXd &z) {
		auto base = sigmoid(z);
		double sum = 0.0;
		for (int i = 0; i < base.rows(); ++i) {
			for (int j = 0; j < base.cols(); ++j) {
				sum += base(i, j);
			}
		}
		for (int i = 0; i < base.rows(); ++i) {
			for (int j = 0; j < base.cols(); ++j) {
				base(i, j) = base(i, j) / sum;
			}
		}
		return base;
	}
};

class Predict {
public:
	Eigen::MatrixXd outputFN(const Eigen::MatrixXd &z) {
		//Eigen::MatrixXd result(z.rows(), z.cols());
		/*for (int i = 0; i < z.rows(); i++) {
			for (int j = 0; j < z.cols(); j++) {
				result(i, j) = z(i, j);
			}
		}*/
		return z;
	}
};
#endif