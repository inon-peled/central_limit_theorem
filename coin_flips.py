import functools
import random
import itertools
import matplotlib.pyplot as plt


def flip(num_flips):
    return map(lambda x: random.choice([0, 1]), range(num_flips))


def distribution_num_heads(num_samples, num_flips_per_sample):
    dist = [0] * (num_flips_per_sample + 1)
    for i in range(num_samples):
        dist[sum(flip(num_flips_per_sample))] += 1
    return dist


def delimit(sequence_of_ones_and_zeros):
    last_element = None
    for index, element in enumerate(sequence_of_ones_and_zeros):
        if last_element is not None and element != last_element:
            yield index - 1
        last_element = element
    yield index


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
    dist = distribution_function(num_samples, num_flips_per_sample)
    open('dist.csv', 'w').write('\n'.join(map(str, enumerate(dist))) + '\n')
    dist_non_zero = list(filter(lambda i_v: i_v[1] != 0, enumerate(dist)))
    min_x, max_x = dist_non_zero[0][0], dist_non_zero[-1][0]
    print(min_x, max_x)
    plt.bar(range(min_x, max_x + 1), dist[min_x:max_x + 1], log=True)
    plt.savefig('dist.png')


if __name__ == '__main__':
    # print(list(delimit('11100110000')))
    experiment_and_plot(distribution_average_repeated_result_length, 1000000, 100)
