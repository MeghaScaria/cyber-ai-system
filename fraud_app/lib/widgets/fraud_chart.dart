import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';

class FraudChart extends StatelessWidget {
  final List<double> data;

  const FraudChart({
    super.key,
    required this.data,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return SizedBox(
      height: 180, // ✅ controlled height (no overflow)
      child: LineChart(
        LineChartData(
          minY: 0,
          maxY: 100,

          gridData: FlGridData(show: false),
          borderData: FlBorderData(show: false),
          titlesData: FlTitlesData(show: false),

          lineBarsData: [
            LineChartBarData(
              // 🔥 SMOOTH CURVE UPGRADE
              isCurved: true,
              curveSmoothness: 0.4,

              color: theme.primaryColor,
              barWidth: 3,

              spots: _buildSpots(),

              dotData: FlDotData(show: false),

              belowBarData: BarAreaData(
                show: true,
                color: theme.primaryColor.withOpacity(0.2),
              ),
            ),
          ],
        ),
      ),
    );
  }

  // 🔹 Convert List → Chart points
  List<FlSpot> _buildSpots() {
    return List.generate(
      data.length,
      (i) => FlSpot(i.toDouble(), data[i]),
    );
  }
}