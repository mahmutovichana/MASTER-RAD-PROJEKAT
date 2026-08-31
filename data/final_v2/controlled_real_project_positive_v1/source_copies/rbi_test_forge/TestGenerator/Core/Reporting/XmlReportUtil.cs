using System.Text;
using System.Xml;
using System.Xml.Linq;

namespace RBBH.TestAutomation.Core.Reporting;

/// <summary>Pomoćne metode za XML formattere (JUnit/TRX) — serializacija s UTF-8 deklaracijom.</summary>
internal static class XmlReportUtil
{
    /// <summary>
    /// Serializuje <see cref="XDocument"/> u string s <c>&lt;?xml ... encoding="utf-8"?&gt;</c>
    /// deklaracijom i uvlačenjem. <see cref="XDocument.ToString()"/> izostavlja deklaraciju,
    /// a obični <c>StringWriter</c> bi prijavio <c>utf-16</c> — zato koristimo UTF-8 writer.
    /// </summary>
    public static string ToXmlString(XDocument doc)
    {
        using var writer = new Utf8StringWriter();
        var settings = new XmlWriterSettings
        {
            Indent = true,
            Encoding = Encoding.UTF8,
            OmitXmlDeclaration = false,
        };
        using (var xml = XmlWriter.Create(writer, settings))
        {
            doc.Save(xml);
        }
        return writer.ToString();
    }

    private sealed class Utf8StringWriter : StringWriter
    {
        public override Encoding Encoding => Encoding.UTF8;
    }
}
