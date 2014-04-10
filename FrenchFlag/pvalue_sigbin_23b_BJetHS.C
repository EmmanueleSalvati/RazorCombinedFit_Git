{
//=========Macro generated from canvas: c1/c1
//=========  (Wed Apr  9 21:59:39 2014) by ROOT version5.34/18
   TCanvas *c1 = new TCanvas("c1", "c1",0,44,600,400);
   gStyle->SetOptStat(0);
   gStyle->SetOptTitle(0);
   c1->SetHighLightColor(2);
   c1->Range(0,0,1,1);
   c1->SetFillColor(0);
   c1->SetBorderMode(0);
   c1->SetBorderSize(2);
   c1->SetLogz();
   c1->SetLeftMargin(0.15);
   c1->SetBottomMargin(0.15);
   c1->SetFrameBorderMode(0);
   Double_t xAxis1[8] = {450, 550, 700, 900, 1200, 1600, 2500, 4000}; 
   Double_t yAxis1[8] = {0.1, 0.2, 0.3, 0.41, 0.52, 0.64, 0.8, 1.5}; 
   
   TH2D *h_23b = new TH2D("h_23b","",7, xAxis1,7, yAxis1);
   h_23b->SetBinContent(10,0.3382177);
   h_23b->SetBinContent(11,0.02688011);
   h_23b->SetBinContent(12,0.5315796);
   h_23b->SetBinContent(13,0.1008666);
   h_23b->SetBinContent(14,0.3267891);
   h_23b->SetBinContent(15,0.6881937);
   h_23b->SetBinContent(16,0.999);
   h_23b->SetBinContent(19,0.8827989);
   h_23b->SetBinContent(20,0.1948285);
   h_23b->SetBinContent(21,0.2698436);
   h_23b->SetBinContent(22,0.999);
   h_23b->SetBinContent(23,0.999);
   h_23b->SetBinContent(24,0.999);
   h_23b->SetBinContent(25,0.999);
   h_23b->SetBinContent(28,0.4752004);
   h_23b->SetBinContent(29,0.5110767);
   h_23b->SetBinContent(30,0.9233403);
   h_23b->SetBinContent(31,0.2653885);
   h_23b->SetBinContent(32,0.999);
   h_23b->SetBinContent(33,0.999);
   h_23b->SetBinContent(34,0.999);
   h_23b->SetBinContent(37,0.793944);
   h_23b->SetBinContent(38,0.2214358);
   h_23b->SetBinContent(39,0.999);
   h_23b->SetBinContent(40,0.1574168);
   h_23b->SetBinContent(41,0.999);
   h_23b->SetBinContent(42,0.999);
   h_23b->SetBinContent(43,0.999);
   h_23b->SetBinContent(46,0.2297571);
   h_23b->SetBinContent(47,0.242915);
   h_23b->SetBinContent(48,0.999);
   h_23b->SetBinContent(49,0.999);
   h_23b->SetBinContent(50,0.999);
   h_23b->SetBinContent(51,0.999);
   h_23b->SetBinContent(52,0.999);
   h_23b->SetBinContent(55,0.999);
   h_23b->SetBinContent(56,0.999);
   h_23b->SetBinContent(57,0.999);
   h_23b->SetBinContent(58,0.999);
   h_23b->SetBinContent(59,0.999);
   h_23b->SetBinContent(60,0.999);
   h_23b->SetBinContent(61,0.999);
   h_23b->SetBinContent(64,0.2014099);
   h_23b->SetBinContent(65,0.999);
   h_23b->SetBinContent(66,0.999);
   h_23b->SetBinContent(67,0.999);
   h_23b->SetBinContent(68,0.999);
   h_23b->SetBinContent(69,0.999);
   h_23b->SetBinContent(70,0.999);
   h_23b->SetMinimum(0);
   h_23b->SetMaximum(1);
   h_23b->SetEntries(49);

   Int_t ci;   // for color index setting
   ci = TColor::GetColor("#000099");
   h_23b->SetLineColor(ci);
   h_23b->GetXaxis()->SetTitle("M_{R}[GeV]");
   h_23b->GetXaxis()->SetLabelFont(42);
   h_23b->GetXaxis()->SetLabelSize(0.065);
   h_23b->GetXaxis()->SetTitleSize(0.065);
   h_23b->GetXaxis()->SetTitleFont(42);
   h_23b->GetYaxis()->SetTitle("R^{2}");
   h_23b->GetYaxis()->SetLabelFont(42);
   h_23b->GetYaxis()->SetLabelSize(0.065);
   h_23b->GetYaxis()->SetTitleSize(0.065);
   h_23b->GetYaxis()->SetTitleFont(42);
   h_23b->GetZaxis()->SetLabelFont(42);
   h_23b->GetZaxis()->SetLabelSize(0.035);
   h_23b->GetZaxis()->SetTitleSize(0.035);
   h_23b->GetZaxis()->SetTitleFont(42);
   h_23b->Draw("colz");
   TLine *line = new TLine(450,0.2,4000,0.2);

   ci = TColor::GetColor("#cccccc");
   line->SetLineColor(ci);
   line->SetLineStyle(2);
   line->Draw();
   line = new TLine(450,0.3,4000,0.3);

   ci = TColor::GetColor("#cccccc");
   line->SetLineColor(ci);
   line->SetLineStyle(2);
   line->Draw();
   line = new TLine(450,0.41,4000,0.41);

   ci = TColor::GetColor("#cccccc");
   line->SetLineColor(ci);
   line->SetLineStyle(2);
   line->Draw();
   line = new TLine(450,0.52,4000,0.52);

   ci = TColor::GetColor("#cccccc");
   line->SetLineColor(ci);
   line->SetLineStyle(2);
   line->Draw();
   line = new TLine(450,0.64,4000,0.64);

   ci = TColor::GetColor("#cccccc");
   line->SetLineColor(ci);
   line->SetLineStyle(2);
   line->Draw();
   line = new TLine(450,0.8,4000,0.8);

   ci = TColor::GetColor("#cccccc");
   line->SetLineColor(ci);
   line->SetLineStyle(2);
   line->Draw();
   line = new TLine(550,0.1,550,1.5);

   ci = TColor::GetColor("#cccccc");
   line->SetLineColor(ci);
   line->SetLineStyle(2);
   line->Draw();
   line = new TLine(700,0.1,700,1.5);

   ci = TColor::GetColor("#cccccc");
   line->SetLineColor(ci);
   line->SetLineStyle(2);
   line->Draw();
   line = new TLine(900,0.1,900,1.5);

   ci = TColor::GetColor("#cccccc");
   line->SetLineColor(ci);
   line->SetLineStyle(2);
   line->Draw();
   line = new TLine(1200,0.1,1200,1.5);

   ci = TColor::GetColor("#cccccc");
   line->SetLineColor(ci);
   line->SetLineStyle(2);
   line->Draw();
   line = new TLine(1600,0.1,1600,1.5);

   ci = TColor::GetColor("#cccccc");
   line->SetLineColor(ci);
   line->SetLineStyle(2);
   line->Draw();
   line = new TLine(2500,0.1,2500,1.5);

   ci = TColor::GetColor("#cccccc");
   line->SetLineColor(ci);
   line->SetLineStyle(2);
   line->Draw();
   c1->Modified();
   c1->cd();
   c1->SetSelected(c1);
}
