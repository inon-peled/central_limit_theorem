import functools
import random
import itertools
import collections
import matplotlib.pyplot as plt


def flip(num_flips):
    return map(lambda x: random.choice([0, 1]), range(num_flips))


def distribution_num_heads(num_samples, num_flips_per_sample):
    flips = map(sum(flip(num_flips_per_sample), range(num_samples)))
    return collections.Counter(flips)


def delimit(sequence_of_ones_and_zeros):
    t = itertools.tee(sequence_of_ones_and_zeros)
    z = itertools.zip_longest(t[0], itertools.islice(t[1], 1, None))
    return map(lambda pair: pair[0],
               filter(lambda pair: pair[1][0] != pair[1][1], enumerate(z)))


def distribution_average_repeated_result_length(num_samples, num_flips_per_sample):
    dist = [0] * ((num_flips_per_sample + 1) * 100)
    for i in range(num_samples):
        flips = flip(num_flips_per_sample)
        d1, d2 = itertools.tee(delimit(flips))
        lengths = itertools.starmap(lambda start, end: end - start,
                                    zip(d1, itertools.islice(d2, 1, None)))
        avg_length = functools.reduce(
            lambda numelem_avg, index_length:
            (index_length[0] + 1, (numelem_avg[0] * numelem_avg[1] + index_length[1]) / (index_length[0] + 1)),
            enumerate(lengths),
            (0, 0.0)
        )[1]
        dist[round(avg_length * 100)] += 1
    return dist


def experiment_and_plot(distribution_function, num_samples, num_flips_per_sample):
    dist = list(distribution_function(num_samples, num_flips_per_sample))
    open('dist.csv', 'w').write('\n'.join(map(str, enumerate(dist))) + '\n')
    dist_non_zero = list(filter(lambda i_v: i_v[1] != 0, enumerate(dist)))
    min_x, max_x = dist_non_zero[0][0], dist_non_zero[-1][0]
    print(min_x, max_x)
    plt.bar(range(min_x, max_x + 1), dist[min_x:max_x + 1], log=True)
    plt.savefig('dist.png')


if __name__ == '__main__':
    print(list(delimit('11100110000')))
    experiment_and_plot(distribution_average_repeated_result_length, 100000, 100)
