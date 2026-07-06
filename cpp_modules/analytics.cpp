#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <cstdlib>

using namespace std;

// High-performance analysis of student prep metrics
int main(int argc, char* argv[]) {
    // Expected CLI arguments:
    // argv[1]: dsa_count (int)
    // argv[2]: streak_count (int)
    // argv[3]: aptitude_pct (int, e.g. 80)
    // argv[4]: fitness_count (int)

    int dsa_count = 0;
    int streak_count = 0;
    int aptitude_pct = 0;
    int fitness_count = 0;

    if (argc >= 5) {
        dsa_count = atoi(argv[1]);
        streak_count = atoi(argv[2]);
        aptitude_pct = atoi(argv[3]);
        fitness_count = atoi(argv[4]);
    }

    // Algorithm to calculate rating (0 to 100)
    double score = (dsa_count * 2.5) + (streak_count * 3.0) + (aptitude_pct * 0.4) + (fitness_count * 5.0);
    if (score > 100.0) score = 100.0;
    if (score < 0.0) score = 0.0;

    string status = "Novice Prep Status";
    string color = "#ef4444"; // Red
    string tip = "Start logging your coding practices, workouts, and solve some DSA problems daily.";

    if (score >= 80.0) {
        status = "Elite Candidate ready for FAANG!";
        color = "#10b981"; // Green
        tip = "Excellent progress! Focus on mock interviewing and high-level system design topics.";
    } else if (score >= 50.0) {
        status = "Solid Candidate";
        color = "#f59e0b"; // Amber
        tip = "Good consistency. Increase LeetCode Medium/Hard problems frequency and finish your aptitude tests.";
    } else if (score >= 20.0) {
        status = "Developing Candidate";
        color = "#3b82f6"; // Blue
        tip = "Keep solving DSA problems. Try to build a consistent 7-day streak to unlock week warrior badges.";
    }

    // Output JSON string directly to stdout for python to process
    cout << "{"
         << "\"success\": true,"
         << "\"score\": " << (int)score << ","
         << "\"status\": \"" << status << "\","
         << "\"color\": \"" << color << "\","
         << "\"recommendation\": \"" << tip << "\""
         << "}" << endl;

    return 0;
}
