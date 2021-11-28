import 'package:http/http.dart';

Future fetchData(String url) async {
  Response response = await get(Uri.parse(url));
  return response.body;
}
