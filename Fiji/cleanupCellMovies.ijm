// movie clean up macro to use prior to segmentation.
// - 1) rescales intensity in the stack so that the max value is 10,000. 
		// this ensures that the subsequent math operation are not limited by the 
		// digitization (i.e. if pixel values are within 100 and 105, averages will
		// be inaccurate because they will be forced to use int values)
// - 2) performs a gaussian blur first with radius gaussRadius (suggested value: 3)
// - 3) performs a sliding average over nSlides (suggested value: 7)
		// slices at the beginning (resp end) of the movie are identical, set to the 
		// first (resp last) slice for which a full nSlice window centered on the slice exists.
		// eg for nSlice = 7, 
		// the first slice surrounded by a full window is slice 4 (starting from slice 1)
		// and the last slice surrounded by a full window is slice 193 (if th movie has 196 slices)
		// so slices 1-4 will be identical; so will be slices 193-196.

macro "cleanup movie"{
	gaussRadius = 3;
	nSlides = 7;
	
	// will only work for single channel images
	setBatchMode(true);
	inputImg = getTitle();
	
	//multiplication factor to avoid digitization when the intensity levels are low
	run("Z Project...", "projection=[Max Intensity]");
	rename("mp");
	getStatistics(area, mean, min, max, std, histogram);
	close("mp");
	
	multFactor = 10000/max;
	selectWindow(inputImg);
	run("Duplicate...", "title=tmp duplicate");
	run("Multiply...", "value="+multFactor+" stack");
	
	// clean up w gaussian blur
	run("Gaussian Blur...", "sigma="+gaussRadius+" stack");
	rename("gauss");
	
	// generate a sliding average across n slides
	n1 = Math.floor(nSlides/2);
	n2 = nSlides - n1 -1;
	print("n1: "+n1+"; n2 = "+n2);
	
	// generate a duplicate stack with same size
	selectWindow("gauss");
	getDimensions(w, h, c, nzs, f);
	
	newImage("slidingAvg", "16-bit Black", w, h, f);
	print(" ");
	print("Starting sliding average...");
	for (i = n1+1; i <= f-n2; i++) {
		selectWindow("gauss");
		iStart = i-n1; 
		iEnd = i+n2;
		print("i: "+i+"; iStart: "+iStart+"; iEnd: "+iEnd);
		run("Duplicate...", "title=tmp duplicate range="+iStart+"-"+iEnd);
		run("Z Project...", "projection=[Average Intensity]");
		rename("tmpAvg");
		run("Select All");
		setPasteMode("Copy");
		run("Copy");
		
		selectWindow("slidingAvg");
		Stack.setPosition(1, i, 1);
		setPasteMode("Copy");
		run("Paste");
		
		close("tmp");
		close("tmpAvg");
	}
	
	//pad with duplicate images at the begining
	selectWindow("slidingAvg");
	firstFullSlice = n1+1;
	Stack.setPosition(1, firstFullSlice, 1);
	run("Select All");
	setPasteMode("Copy");
	run("Copy");
	for(i = 1; i <= n1; i++) {
		print("i: "+i+"; set to slice n1+1: "+firstFullSlice);
		selectWindow("slidingAvg");
		Stack.setPosition(1, i, 1);
		setPasteMode("Copy");
		run("Paste");
	}
	// pad with duplicate images at the end
	selectWindow("slidingAvg");
	lastFullSlice = f-n2;
	Stack.setPosition(1, lastFullSlice, 1);
	run("Select All");
	setPasteMode("Copy");
	run("Copy");
	for(i = f-n2+1; i <= f; i++) {
		print("i: "+i+"; set to slice f-n2: "+lastFullSlice);
		selectWindow("slidingAvg");
		Stack.setPosition(1, i, 1);
		setPasteMode("Copy");
		run("Paste");
	}
	rename("slidingAvg"+nSlides);
	close("gauss");
	setBatchMode("exit and display");
	
	
}


run("Gaussian Blur...", "sigma=3 stack");
run("Duplicate...", "duplicate");
selectWindow("MAX_HS_Long_lowPower-196int_100s_10ms_1_MMStack_Pos1_stitch.ome.tif");
run("Duplicate...", "duplicate");
selectWindow("MAX_HS_Long_lowPower-196int_100s_10ms_1_MMStack_Pos1_stitch.ome-5.tif");
rename("1");
selectWindow("MAX_HS_Long_lowPower-196int_100s_10ms_1_MMStack_Pos1_stitch.ome-6.tif");
rename("2");
selectWindow("MAX_HS_Long_lowPower-196int_100s_10ms_1_MMStack_Pos1_stitch.ome.tif");
run("Duplicate...", "title=3 duplicate");

