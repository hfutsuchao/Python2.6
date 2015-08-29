def movingAverageExponential(values, alpha, epsilon = 0):
 if not 0 < alpha < 1:
  raise ValueError("out of range, alpha='%s'" % alpha)
 if not 0 <= epsilon < alpha:
  raise ValueError("out of range, epsilon='%s'" % epsilon)
 result = [None] * len(values)
 for i in range(len(result)):
  currentWeight = 1.0
  numerator  = 0
  denominator = 0
  for value in values[i::-1]:
    numerator  += value * currentWeight
    denominator += currentWeight
    currentWeight *= alpha
    if currentWeight < epsilon: 
      break
  result[i] = numerator / denominator
  return result

values = [3,1,1,1,2,1,1,1,1,33,1,2]
print movingAverageExponential(values,2.0/13.0)