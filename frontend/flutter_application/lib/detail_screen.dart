import 'package:flutter/material.dart';

class DetailScreen extends StatelessWidget {
  final String imageUrl;
  final String date;
  final String description;

  DetailScreen({required this.imageUrl, required this.date, required this.description});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Intrusion Details'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Image.network(
              imageUrl,
              height: 200,
            ),
            SizedBox(height: 20),
            Text(
              'Date: $date',
              style: TextStyle(fontSize: 20),
            ),
            SizedBox(height: 10),
            Text(
              'Description: $description',
              style: TextStyle(fontSize: 16),
            ),
          ],
        ),
      ),
    );
  }
}
