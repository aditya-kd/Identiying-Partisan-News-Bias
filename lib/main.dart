import 'package:flutter/material.dart';
import 'package:news_mark1/colors.dart';
import 'package:news_mark1/theme.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(theme: lightTheme, home: SafeArea(child: MyHomePage()));
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({Key? key}) : super(key: key);

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  final searchController = TextEditingController();
  @override
  void initState() {
    super.initState();
    searchController.addListener(() {
      String op = searchController.text;
      print('Currently Typed: $op');
    });
  }

  @override
  void dispose() {
    searchController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        backgroundColor: Colors.grey[850],
        appBar: AppBar(
          title: Text('News'),
          actions: [
            IconButton(
                onPressed: () {
                  print('Settings Tapped');
                },
                icon: Icon(Icons.settings))
          ],
        ),
        body: Padding(
            padding: EdgeInsets.all(8.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.start,
                  children: [
                    Text(
                      'We report to\nYOU.',
                      style: TextStyle(color: Colors.white, fontSize: 24),
                    ),
                  ],
                ),
                TextField(
                  onSubmitted: (text) {
                    print('Submitted Query: $text');
                  },
                  enableSuggestions: true,
                  controller: searchController,
                  style: TextStyle(color: primary),
                  decoration: InputDecoration(
                    filled: true,
                    fillColor: Colors.white54,
                    focusColor: Colors.white,
                    suffixIcon: Icon(Icons.search),
                    hintStyle: TextStyle(color: Color(0xff3C3535)),
                    border: OutlineInputBorder(
                        borderRadius: BorderRadius.all(Radius.circular(50))),
                    hintText: 'Search',
                  ),
                ),
                ElevatedButton(
                    style: ElevatedButton.styleFrom(
                        padding: EdgeInsets.symmetric(
                            horizontal: 28.0, vertical: 10),
                        shape: RoundedRectangleBorder(
                            borderRadius:
                                BorderRadius.all(Radius.circular(10.0)))),
                    onPressed: () {
                      print('Searched for: ${searchController.text}');
                    },
                    child: Text(
                      'Search',
                      style: TextStyle(fontSize: 16),
                    )),
              ],
            )));
  }
}
