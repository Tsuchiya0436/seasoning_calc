from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import SeasoningModel
import re


class SeasoningMenu(ListView):
    template_name = 'menu.html'
    model = SeasoningModel
    
    def get_seasoning_list(self):
        return SeasoningModel.objects.all()

    
class SeasoningCalculation(ListView):
    template_name = 'calculator.html'
    
    def get_seasoning_list(self):
        return SeasoningModel.objects.all()

    
    def search_seasonings(self, seasoning_name, seasoning_list):
        hira_pattern = re.compile('^[ぁ-ん]+$')
        if hira_pattern.fullmatch(seasoning_name):
            return list(seasoning_list.filter(hiraname__icontains=seasoning_name))
        else:
            return list(seasoning_list.filter(name__icontains=seasoning_name))
       

    def calculate_seasoning_amounts(self, seasoning, amount, times, quantity):
        if amount == 'tbsp' and seasoning.tbsp:
            return{'value':seasoning.tbsp * quantity * times}
        elif amount == 'tsp' and seasoning.tsp:
            return{'value':seasoning.tsp * quantity * times}
        else:
            return {'value': -1.0}
                

    def get(self, request, *args, **kwargs):
        seasoning_list = self.get_seasoning_list()
        quantity_str = self.request.GET.get('multiple') or '0'
        try:
            quantity = float(quantity_str)
        except ValueError:
            quantity = 0.0

        seasoning_calculations = {}
        for i in range(1, 6):
            seasoning_name = self.request.GET.get(f'seasoning_{i}')
            seasoning_amount = self.request.GET.get(f'amount_{i}')
            times_str = self.request.GET.get(f'times_{i}') or '0'
            try:
                seasoning_times = int(times_str)
            except ValueError:
                seasoning_times = 0

            if seasoning_name and seasoning_amount:
                searched_seasonings = self.search_seasonings(seasoning_name, seasoning_list)
                for seasoning in searched_seasonings:
                    seasoning_dict = self.calculate_seasoning_amounts(seasoning, seasoning_amount, seasoning_times, quantity)
                    if seasoning_dict['value'] != -1.0:
                        seasoning_calculations[seasoning_name] = {
                            'amount':seasoning_amount,
                            'times':seasoning_times,
                            **seasoning_dict
                        }

        return render(request, self.template_name, {
            'seasoning_list': seasoning_list,
            'seasoning_calculations': seasoning_calculations,
            'quantity': quantity
        })

    
class SeasoningList(ListView):
    template_name = 'list.html'
    
    def get_queryset(self):
        return SeasoningModel.objects.all()