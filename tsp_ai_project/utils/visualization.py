import matplotlib.pyplot as plt
import os
import re  # أضف ده في الأول لو مش موجود


def plot_tour(cities, tour, title):
    """Plot the cities and the tour."""
    if not os.path.exists('results'):
        os.makedirs('results')

    # تنظيف الـ title من أي حروف ممنوعة في Windows
    safe_title = re.sub(r'[<>:"/\\|?*]', '', title)  # حذف الحروف الممنوعة
    safe_title = safe_title.replace(' ', '_')  # مسافات لـ _

    plt.figure()
    plt.scatter(cities[:, 0], cities[:, 1])
    tour_points = cities[tour]
    plt.plot(tour_points[:, 0], tour_points[:, 1], 'r-')
    plt.title(title)
    plt.savefig(f'results/{safe_title}.png')
    plt.close()