Subject: Follow-up on c_delta and the proposed c_delta_star

Dear Professor Hoorn,

Thank you very much for the detailed note. Your distinction helped me clarify that the Huber-centre version has indeed changed the research question. I agree that it should be treated as a separate c_delta_star: a salience-profile concordance statistic concerned with whether the same individual is atypical across two measures or occasions, rather than simply a robust replacement for the original c_delta.

I have now completed several focused checks in response to your questions.

First, Pearson correlation between the robust absolute residual profiles gives exactly the same one-sided permutation evidence as c_delta_star. Algebraically,

c_delta_star = 1 + r_Pearson CV_X CV_Y.

Because the two CV terms remain fixed under permutations of the pairing, the permutation ordering and p-value are identical. Dividing the residuals by their MAD scales also makes no difference to either statistic. The numerical value is not identical, however: Pearson isolates concordance, whereas c_delta_star also incorporates the marginal heterogeneity of the two salience profiles through CV_X CV_Y. This seems to make the scientific status of that weighting the next important definition question.

Second, Mantel and the original c_delta do not preserve the same information. Mantel compares the complete set of corresponding dyadic distances. The original c_delta compresses each distance matrix to one overall-divergence value per labelled observation. I constructed data for which the two c_delta divergence profiles were identical and their profile correlation was always 1, while the mean Mantel correlation was only about .231. I therefore think the cross-building claim should be narrowed: c_delta can compare whether the same rooms are globally divergent in corresponding systems, but it does not establish that the complete pairwise disease and ventilation geometries are the same. MRQAP or a building-level interaction permutation would be closer if the full dyadic relationship is the target.

Third, I agree with your distinction between describing this exact team and generalising to a representative team type. A meaningful exceptional member should not automatically be removed. However, inclusion and leverage are separate questions. In the new simulations, the Huber centre protected the ordinary observations, but the uncapped c_delta_star could concentrate even more strongly on one matched extreme observation: at magnitude 32, the largest observation contributed a median .965 of the numerator, compared with .474 for the original L2 c_delta. Thus the uncapped version has a robust reference centre but not bounded final influence. The cap-6 version remains useful as a separate sensitivity estimand.

I have attached a technical note containing the definitions, exact Pearson identity, Mantel comparison, cross-building permutation results, outlier simulations, and the recent influence-function and interval findings. My current recommendation is to retain both research questions explicitly: original c_delta for exact-set L2 divergence-profile concordance, and c_delta_star for robust-centre salience-profile concordance, with cap 6 reported separately when bounded final leverage is required.

Please let me know whether this distinction reflects what you had in mind. If so, my next step will be a common building-style simulation comparing original c_delta, c_delta_star, Pearson profile correlation, and Mantel/MRQAP under node-salience and dyadic alternatives.

Kind regards,

Jialiang
