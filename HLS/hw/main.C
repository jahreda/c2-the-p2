#include "main.h"
#include <ap_int.h>
#include <ap_fixed.h> // Using fixed-point arithmetic for resource optimization
#include <hls_stream.h>
#include <iostream>  // For debug prints
#include "hls_math.h"
#include <fstream>
#include <iomanip>
#include <cstring>
#include <string>
#include "fit.h"

using namespace std;

int main() {
	fit(tempxs, tempys, tempsigmas, templasts, tempN);
	return 0;
}
