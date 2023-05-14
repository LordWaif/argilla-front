function weightedMovingAverage(array, period) {
    const w = new Array(period).fill(1);
    const ma = [];
  
    for (let i = period; i <= array.length; i++) {
      const values = array.slice(i - period, i);
      const weightedSum = values.reduce((acc, val, j) => acc + val * w[j], 0);
      const weightsSum = w.reduce((acc, val) => acc + val, 0);
      const weightedAverage = weightedSum / weightsSum;
      ma.push(weightedAverage);
    }
    if(ma.length == 0){
      ma.push(0);
    }
    console.log(ma)
    return ma;
  }
  