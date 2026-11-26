#include <iostream>
#include <iterator>
#include <map>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int operation_count;
    if (!(std::cin >> operation_count)) {
        return 0;
    }

    // Stored closed intervals are disjoint and ordered by their left endpoint.
    std::map<int, int> intervals;
    for (int i = 0; i < operation_count; ++i) {
        char operation;
        std::cin >> operation;
        if (operation == 'B') {
            std::cout << intervals.size() << '\n';
            continue;
        }

        int left, right;
        std::cin >> left >> right;
        auto current = intervals.lower_bound(left);
        if (current != intervals.begin()) {
            auto previous = std::prev(current);
            if (previous->second >= left) {
                current = previous;
            }
        }

        int removed = 0;
        while (current != intervals.end() && current->first <= right) {
            current = intervals.erase(current);
            ++removed;
        }
        intervals.emplace_hint(current, left, right);
        std::cout << removed << '\n';
    }
}
