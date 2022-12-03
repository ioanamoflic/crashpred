data {
  int<lower=0> N;
  int<lower=0> M;
  int success[N, M];
  int attempts[N, M];
  int year[N, M];
  int oxygen_used[N, M];
}

parameters {
  real hyper_intercept_mean;
  real hyper_intercept_sd;
  real intercept[M];
  real year_weight;
  real oxygen_weight;
}

transformed parameters {
  real theta[N, M];
  
  for(i in 1:N)
    for(j in 1:M)
    {
      // theta[i, j] = min([1, max( [0, (intercept[j] + year_weight * (year[i, j] - 1980)/8 + oxygen_weight * oxygen_used[i, j])/100 ]) ]);
      theta[i, j] = (intercept[j] + year_weight * (year[i, j] - 1980)/8 + oxygen_weight * oxygen_used[i, j])/100;
    }
      
}

model {
  // hyper prior
  hyper_intercept_mean ~ normal(50, 3); //uniform(-4, 4); //uniform(40, 80); //normal(70, 5);
  hyper_intercept_sd ~ normal(3, 1); //uniform(0, 5); //normal(10, 3);
  
  // priors
  for (i in 1:M){
    intercept[i] ~ normal(hyper_intercept_mean, hyper_intercept_sd);
  }
  
  year_weight ~ normal(2, 1); //uniform(0, 4); //normal(0.4, 0) //normal(4, 0.75); //uniform(0, 5); //normal(0,20);
  oxygen_weight ~ normal(10, 3); //normal(20, 5); //uniform(0, 20); //normal(1,20);
  
  
  // likelihood
  for(i in 1:M)
    success[, i] ~ binomial(attempts[, i], theta[, i]);
}
 
generated quantities {
  matrix[N, M] log_lik;
  
  for(i in 1:N)
    for(j in 1:M)
      log_lik[i, j] = binomial_lpmf( success[i, j] | attempts[i, j], theta[i, j]);
}
