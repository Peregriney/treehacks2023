import 'package:flutter/material.dart';
import 'detail_screen.dart';
import 'dart:convert';
import 'dart:typed_data';
import 'package:http/http.dart' as http;

class HomePage extends StatefulWidget {
  @override
  _HomePageState createState() => _HomePageState();
}


MemoryImage base64Image(String base64String) {
  Uint8List bytes = base64Decode(base64String);
  return MemoryImage(bytes);
}

class _HomePageState extends State<HomePage> {
  @override
  void initState() {
    super.initState();
    _updateImageList();
  }

  List<dynamic> imageList = [];

    void _updateImageList() async {
    String url = 'https://peregriney--yolo-detection-web-dev.modal.run/';


    try {
      http.Response response = await http.get(Uri.parse(url));

      if (response.statusCode == 200) {
        // Parse the JSON response
        Map<String, dynamic> jsonData = json.decode(response.body);

        // Update the imageList state with the new data
        setState(() {
          imageList = jsonData.values.toList();
        });
        print(imageList);
      } else {
        // Handle error
        print('Request failed with status: ${response.statusCode}.');
      }
    } catch (e) {
      // Handle error
      print('Request failed with error: $e.');
    }
  }

  List<String> dateList = [
    "Feb 2, 2023 10:23 AM",
    "Feb 2, 2023 11:45 AM",
    "Feb 2, 2023 12:12 PM",
  ];

  List<String> descriptionList = [
    "NE Barn - Goose",
    "SW Pen - Duck",
    "NW Pen - Duck",
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Recent Notifications'),
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
          Image.memory(
            base64Decode(imageUrl),
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
