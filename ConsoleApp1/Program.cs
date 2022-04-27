using HtmlAgilityPack;
using System;

using System.Collections.Generic;

using System.Net;

using System.Web;

namespace ConsoleApp1
{
    class Program
    {
        static void Main(string[] args)
        {
                try

                {

                    string fromLanguage, toLanguage, text; // create string type of variable

                    text = "hello, I am a human"; // give the text for converting other language

                    fromLanguage = "English"; // form language means source language

                    toLanguage = "Danish"; // to language for converting in this language

                    var language = new Dictionary<string, string>(); // create a Dictionary type  variable

                    Language.LanguageMap(language); // Call the LanuageMap method for initiate the language.

                    Console.WriteLine("Your Text: " + text); // show your raw text on the screen

                    Uri address = new Uri("http://translate.google.com/translate_t"); // create a uri type address named variable and uriString means pass the URL.

                    WebClient webClient = new WebClient();// create the WebClient instance

                    webClient.Headers[HttpRequestHeader.ContentType] = "application/x-www-form-urlencoded"; // Give the Content type for WebClents Headers

                    webClient.UploadStringCompleted += new UploadStringCompletedEventHandler(webClient_UploadStringCompleted); // overload the UploadStringComplete event.

                    webClient.UploadStringAsync(address, GetPostData(language[fromLanguage], language[toLanguage], text)); // this method is uploads the specified string to the specified resorce.

                    Console.ReadKey();

                }

                catch (Exception ex)

                {

                    Console.WriteLine(ex);

                    Console.ReadKey();

                }

            }
        static string GetPostData(string fromLanguage, string toLanguage, string text)

        {

            string data = string.Format("hl=en&ie=UTF8&oe=UTF8submit=Translate&langpair={0}|{1}", fromLanguage, toLanguage); // Here put the language translation for from and to.

            return data += "&text=" + HttpUtility.UrlEncode(text); // Here Encoded the content.

        }

        static void webClient_UploadStringCompleted(object sender, UploadStringCompletedEventArgs e)

        {

            if (e.Result != null) // Check the event result is null or not.

            {

                var document = new HtmlDocument();// create new HtmlDocument to store my page html.

                document.LoadHtml(e.Result); // Now load the getting Html

                var node = document.DocumentNode.SelectSingleNode("//span[@id='result_box']"); // Here finding particular tag to get value from HtmlDocument

                var output = node != null ? node.InnerText : e.Error.Message;

                Console.WriteLine("Translated Text: " + output); // show the output

            }

        }
    }
}
