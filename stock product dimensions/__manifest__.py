{
    "name": "Product Dimensions & Stock All-in-One (Full Views)",
    "version": "1.0",
    "category": "Inventory",
    "author": "UFVdev",
    "summary": "Ajoute les dimensions en mm, et affiche le stock en m²/m³ dans toutes les vues : produits, variantes, quants, analyse stock.",
    "depends": ["stock", "product"],
    "data": [
        "views/product_template_views.xml",
        "views/product_product_views.xml",
        "views/stock_quant_views.xml",
        "views/product_stock_report_views.xml"
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3"
}
