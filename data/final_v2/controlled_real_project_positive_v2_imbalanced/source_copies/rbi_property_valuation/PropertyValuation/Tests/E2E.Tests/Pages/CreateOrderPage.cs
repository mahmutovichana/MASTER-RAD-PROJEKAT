using Microsoft.Playwright;

namespace RBBH.CollateralAppraisal.E2E.Tests.Pages;

public sealed class CreateOrderPage(IPage page)
{
    public async Task GotoFLAsync() =>
        await page.GotoAsync("/narudzbe/nova/FL");

    public async Task GotoPLAsync() =>
        await page.GotoAsync("/narudzbe/nova/PL");

    public async Task FillClientNameAsync(string name) =>
        await page.Locator("#field-clientName input, input[placeholder*='klijent'], input[placeholder*='naziv']")
                  .First.FillAsync(name);

    public async Task FillJmbgAsync(string jmbg) =>
        await page.Locator("#field-jmbg input, input[placeholder*='JMBG']")
                  .First.FillAsync(jmbg);

    public async Task FillContactNameAsync(string name) =>
        await page.Locator("#field-contactName input, input[placeholder*='kontakt']")
                  .First.FillAsync(name);

    public async Task FillPhoneAsync(string phone) =>
        await page.Locator("#field-phone input, input[placeholder*='telefon'], input[type='tel']")
                  .First.FillAsync(phone);

    public async Task FillPropertyAddressAsync(string address) =>
        await page.Locator("#field-propertyAddress input, input[placeholder*='adresa']")
                  .First.FillAsync(address);

    public async Task FillCityAsync(string city) =>
        await page.Locator("#field-city input, input[placeholder*='grad']")
                  .First.FillAsync(city);

    public async Task FillDeliveryContactAsync(string name) =>
        await page.Locator("#field-deliveryContact input, input[placeholder*='dostav']")
                  .First.FillAsync(name);

    public async Task FillAmRecipientAsync(string name) =>
        await page.Locator("#field-amRecipient input, input[placeholder*='primalac']")
                  .First.FillAsync(name);

    public async Task ClickSubmitAsync() =>
        await page.ClickAsync("button.of-btn-submit, button:has-text('Pošalji CA')");

    public async Task ClickSaveDraftAsync() =>
        await page.ClickAsync("button.of-btn-draft, button:has-text('Sačuvaj nacrt')");

    public async Task<bool> IsSubmitEnabledAsync()
    {
        var btn = page.Locator("button.of-btn-submit, button:has-text('Pošalji CA')").First;
        return await btn.IsEnabledAsync();
    }

    public async Task<bool> HasSuccessSnackbarAsync() =>
        await page.GetByText("uspješno", new PageGetByTextOptions { Exact = false })
                  .IsVisibleAsync();

    public async Task FillMinimalFLOrderAsync()
    {
        await FillClientNameAsync("E2E FL Test Klijent");
        await FillContactNameAsync("Kontakt Osoba");
        await FillPhoneAsync("061000001");
        await FillPropertyAddressAsync("Ulica Test 1");
        await FillCityAsync("Sarajevo");
        await FillDeliveryContactAsync("Dostava Osoba");
        await FillAmRecipientAsync("AM Primalac");
    }
}
