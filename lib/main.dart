import 'package:flutter/material.dart';
import 'package:news_mark1/colors.dart';
import 'package:news_mark1/request.dart';
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
                    onPressed: () async {
                      print('Search Query submitted:'+searchController.text);
                      // Navigator.push(context, MaterialPageRoute(builder: ))
                Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => HomeScreen(searchQuery: searchController.text ),
                ));
              
                
          // var parsed = jsonDecode(data);
          // String printableData=makePrintableData(data);
          // setState(() {
          //   displayText = "" + printableData;
          // });  
        },
                    child: Text(
                      'Search',
                      style: TextStyle(fontSize: 16),
                    )),
              ],
            )));
  }
  String makePrintableData(data) {
  //do the processing to remove unwanted JSON stuff
  
  return data;
}

}
class HomeScreen extends StatefulWidget {
  const HomeScreen ({Key? key, required this.searchQuery}) : super(key: key);
  final String searchQuery;

  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  String printableData='No Data till now';

  Future loadNews() async{
    var data =
               await fetchData('http://10.0.2.2:5000/api?query=' + widget.searchQuery);
    //           //await fetchData('http://127.0.0.1:5000/api?query=' +searchQuery);
          // var data =
          //      await fetchData('https://jsonplaceholder.typicode.com/albums/1');
          print('data recieved ,{$data}');
          setState(() {
            printableData=data;
          });
  }

  @override
  Widget build(BuildContext context) {

    loadNews();

    return Scaffold(
      appBar: AppBar(
        title: Text("Home Screen"),
      ),
      body: Center(
        child: Column(children: [
          Row(children: [Text(widget.searchQuery), ],),
          printableData.isEmpty?Text(printableData):Center(child: Text(printableData))

          
        ],)
      ),
    );
  }
}

