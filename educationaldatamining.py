from sklearn.preprocessing import LabelEncoder
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import math


feature_dict = {i:label for i,label in zip(
                range(7),
                  ('famrel',
                  'studytime',
                  'freetime',
                  'goout',
                  'health',
                  'absences',
                  'meanscore'))}

ab=pd.ExcelFile("new.xlsx")
dd=pd.ExcelFile("new.xlsx")
cd=ab.parse("Sheet1")
de=dd.parse("Sheet1")


cd.columns = [l for i,l in sorted(feature_dict.items())] + ['Class']
de.columns=[l for i,l in sorted(feature_dict.items())] + ['Class']


cd.tail()
de.tail()

print(de)

X=de[['famrel','studytime','freetime','goout','health','absences','meanscore']].values
y=de['Class'].values

enc = LabelEncoder()
label_encoder = enc.fit(y)
y = label_encoder.transform(y) + 1

label_dict = {1:'Poor',2:'Average',3:'Good',4:'Excellent'}

#PLOTTING

fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(12,6))

for ax,cnt in zip(axes.ravel(), range(7)):  

    # set bin sizes
    min_b = math.floor(np.min(X[:,cnt]))
    max_b = math.ceil(np.max(X[:,cnt]))
    bins = np.linspace(min_b, max_b, 25)

    # plottling the histograms
    for lab,col in zip(range(1,5), ('blue', 'red', 'green' , 'yellow')):
        ax.hist(X[y==lab, cnt],
                   color=col,
                   label='class %s' %label_dict[lab],
                   bins=bins,
                   alpha=0.5,)
    ylims = ax.get_ylim()

    # plot annotation
    leg = ax.legend(loc='upper right', fancybox=True, fontsize=8)
    leg.get_frame().set_alpha(0.5)
    ax.set_ylim([0, max(ylims)+2])
    ax.set_xlabel(feature_dict[cnt])
    ax.set_title('Student Data histogram #%s' %str(cnt+1))

    # hide axis ticks
    ax.tick_params(axis="both", which="both", bottom="off", top="off",  
            labelbottom="on", left="off", right="off", labelleft="on")

    # remove axis spines
    ax.spines["top"].set_visible(False)  
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)    

axes[0][0].set_ylabel('count')
axes[1][0].set_ylabel('count')

fig.tight_layout()       

plt.show()

#Step 1: Computing the d-dimensional mean vectors
np.set_printoptions(precision=4)

mean_vectors = []
for cl in range(1,5):
    mean_vectors.append(np.mean(X[y==cl], axis=0))
    print('Mean Vector class %s: %s\n' %(cl, mean_vectors[cl-1]))

#Computing the scatter matrices
S_W = np.zeros((7,7))
for cl,mv in zip(range(1,7), mean_vectors):
    class_sc_mat = np.zeros((7,7))                  # scatter matrix for every class
    for row in X[y == cl]:
        row, mv = row.reshape(7,1), mv.reshape(7,1) # make column vectors
        class_sc_mat += (row-mv).dot((row-mv).T)
    S_W += class_sc_mat                             # sum class scatter matrices
print('within-class Scatter Matrix:\n', S_W)

overall_mean = np.mean(X, axis=0)

S_B = np.zeros((7,7))
for i,mean_vec in enumerate(mean_vectors):  
    n = X[y==i+1,:].shape[0]
    mean_vec = mean_vec.reshape(7,1) # make column vector
    overall_mean = overall_mean.reshape(7,1) # make column vector
    S_B += n * (mean_vec - overall_mean).dot((mean_vec - overall_mean).T)

print('between-class Scatter Matrix:\n', S_B)


#Solving the generalized eigen vector problems
eig_vals, eig_vecs = np.linalg.eig(np.linalg.inv(S_W).dot(S_B))

for i in range(len(eig_vals)):
    eigvec_sc = eig_vecs[:,i].reshape(7,1)   
    print('\nEigenvector {}: \n{}'.format(i+1, eigvec_sc.real))
    print('Eigenvalue {:}: {:.2e}'.format(i+1, eig_vals[i].real))

for i in range(len(eig_vals)):
    eigv = eig_vecs[:,i].reshape(7,1)
    np.testing.assert_array_almost_equal(np.linalg.inv(S_W).dot(S_B).dot(eigv),
                                         eig_vals[i] * eigv,
                                         decimal=6, err_msg='', verbose=True)
print('ok')


# Make a list of (eigenvalue, eigenvector) tuples
eig_pairs = [(np.abs(eig_vals[i]), eig_vecs[:,i]) for i in range(len(eig_vals))]

# Sort the (eigenvalue, eigenvector) tuples from high to low
eig_pairs = sorted(eig_pairs, key=lambda k: k[0], reverse=True)

# Visually confirm that the list is correctly sorted by decreasing eigenvalues

print('Eigenvalues in decreasing order:\n')
for i in eig_pairs:
    print(i[0])

print('Variance explained:\n')
eigv_sum = sum(eig_vals)
for i,j in enumerate(eig_pairs):
    print('eigenvalue {0:}: {1:.2%}'.format(i+1, (j[0]/eigv_sum).real))


W = np.hstack((eig_pairs[0][1].reshape(7,1), eig_pairs[1][1].reshape(7,1)))
print('Matrix W:\n', W.real)

X_lda = X.dot(W)
assert X_lda.shape == (395,2), "The matrix is not 395x2 dimensional."

def plot_step_lda():

    ax = plt.subplot(111)
    for label,marker,color in zip(
        range(1,5),('^', 's', 'o','*'),('blue', 'red', 'green','yellow')):

        plt.scatter(x=X_lda[:,0].real[y == label],
                y=X_lda[:,1].real[y == label],
                marker=marker,
                color=color,
                alpha=0.5,
                label=label_dict[label]
                )

    plt.xlabel('LD1')
    plt.ylabel('LD2')

    leg = plt.legend(loc='upper right', fancybox=True)
    leg.get_frame().set_alpha(0.5)
    plt.title('LDA: Student Data projection onto the first 2 linear discriminants')

    # hide axis ticks
    plt.tick_params(axis="both", which="both", bottom="off", top="off",  
            labelbottom="on", left="off", right="off", labelleft="on")

    # remove axis spines
    ax.spines["top"].set_visible(False)  
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)    

    plt.grid()
    plt.tight_layout
    plt.show()

plot_step_lda()