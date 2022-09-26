from wagtail.core import blocks

class GradientDescentWidget(blocks.StructBlock):
    class Meta:
        icon = ""
        label = "Gradient Descent Block"
        admin_text = '{label}: configured elsewhere'.format(label=label)
        template = 'oneoff_blocks/gradient_descent.html'


class StatisticalMurderWidget(blocks.StaticBlock):
    class Meta:
        icon = ""
        label = "Statistical Murder Widget"
        admin_text = '{label}: configured elsewhere'.format(label=label)
        template = 'oneoff_blocks/statistical_murder_widget.html'
