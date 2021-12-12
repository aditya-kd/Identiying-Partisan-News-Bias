import 'package:flutter/material.dart';
import 'package:news_mark1/request.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen ({Key? key, required this.searchQuery}) : super(key: key);
  final String searchQuery;

  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  String printableData='No Data till now';
  String loremIpsum="Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.";
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
        title: Text("News"),
      ),
      body: Padding(
        padding: const EdgeInsets.all(8.0),
        child: Column(children: [
          Flexible(flex: 1,
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Row(children: [Text('Title of News or the Headline'),],
              mainAxisAlignment: MainAxisAlignment.start,),
            ),
          ),
          Flexible(flex:3,
            child: Row(children: [Center(child: Wrap(direction:Axis.horizontal, children:[Text(loremIpsum)]))])),
          Flexible(flex:2,child: Row(children:[Text('What we found')]))
          
          
        ],),
      ),
      // body: Center(
      //   child: Column(children: [
      //     Row(children: [Text(widget.searchQuery), ],),
      //     printableData.isEmpty?Text(printableData):Center(child: Text(printableData))

          
      //   ],)
      // ),
    );
  }
}
