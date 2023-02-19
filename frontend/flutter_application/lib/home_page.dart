import 'package:flutter/material.dart';
import 'detail_screen.dart';

class HomePage extends StatefulWidget {
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  List<String> imageList = [
    "https://via.placeholder.com/150",
    "https://via.placeholder.com/150",
    "https://via.placeholder.com/150",
    "https://via.placeholder.com/150",
    "https://via.placeholder.com/150",
  ];

  List<String> dateList = [
    "Feb 1, 2023 10:00 AM",
    "Feb 2, 2023 11:00 AM",
    "Feb 3, 2023 12:00 PM",
    "Feb 4, 2023 1:00 PM",
    "Feb 5, 2023 2:00 PM",
  ];

  List<String> descriptionList = [
    "Description 1",
    "Description 2",
    "Description 3",
    "Description 4",
    "Description 5",
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Flutter App'),
      ),
      body: ListView.builder(
        itemCount: imageList.length,
        itemBuilder: (context, index) {
          return GestureDetector(
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => DetailScreen(
                    imageUrl: imageList[index],
                    date: dateList[index],
                    description: descriptionList[index],
                  ),
                ),
              );
            },
            child: ListItem(
              imageUrl: imageList[index],
              date: dateList[index],
              description: descriptionList[index],
            ),
          );
        },
      ),
    );
  }
}

class ListItem extends StatelessWidget {
  final String imageUrl;
  final String date;
  final String description;

  ListItem({
    required this.imageUrl,
    required this.date,
    required this.description,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.all(8.0),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Image.network(
            imageUrl,
            width: 150,
            height: 100,
          ),
          SizedBox(width: 8.0),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  date,
                  style: TextStyle(
                    fontWeight: FontWeight.bold,
                    fontSize: 16.0,
                  ),
                ),
                SizedBox(height: 8.0),
                Text(
                  description,
                  style: TextStyle(fontSize: 16.0),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
