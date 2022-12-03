data {
  int<lower=0> N;
  int success[N];
  int attempts[N];
  int year[N];
  int oxygen_used[N];
}

parameters {
  real intercept;
  real year_weight;
  real oxygen_weight;
}

transformed parameters {
  real theta[N];
  for(i in 1:N)
    theta[i] = (intercept + year_weight * (year[i]-1980)/8 + oxygen_weight * oxygen_used[i])/100;
}

model {
  
  // priors
  intercept ~ normal(50, 10); // uniform(20, 40); //normal(40,20);
  year_weight ~ normal(4, 0.75); //uniform(0, 5); //normal(0,20);
  oxygen_weight ~  normal(20, 5); //uniform(0, 20); //normal(1,20);
  
  
  // likelihood
  success ~ binomial(attempts, theta);
}
 
generated quantities {
  vector[N] log_lik;
  for(i in 1:N)
    log_lik[i] = binomial_lpmf( success[i] | attempts[i], theta[i]);
}
