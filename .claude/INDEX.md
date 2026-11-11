# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
 10800  GET              /                                                dashboard
 12857  GET              /api/abo/status                                  api_abo_status
 12811  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 11588  GET              /api/automation/status                           api_automation_status
 11610  POST             /api/automation/toggle                           api_automation_toggle
 21185  GET              /api/channel/categories                          api_channel_categories
 21191  POST             /api/channel/set                                 api_channel_set
 21038  GET              /api/channels/status                             api_channels_status
 20712  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 20695  GET              /api/clips                                       api_clips
 20741  POST/DELETE      /api/clips/clear                                 api_clips_clear
 20613  GET              /api/debug/threads                               api_debug_threads
 12822  GET              /api/events                                      api_events
 12301  GET              /api/events/stream                               api_events_stream
 12128  GET              /api/health                                      api_health
 20654  POST             /api/highlights/config                           api_highlights_config
 10730  POST             /api/login                                       dashboard_login_submit
 13147  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 12216  GET              /api/notify/status                               api_notify_status
 12227  POST             /api/notify/test                                 api_notify_test
 12911  GET              /api/proxy/heatmap                               api_proxy_heatmap
 12888  GET              /api/proxy/trend                                 api_proxy_trend
 20761  GET              /api/tts/<fn>                                    api_tts_file
 21535  GET              /api/upload_window                               api_upload_window
 12418  GET              /archive/<int:eid>/download                      archive_download
 12446  GET              /download/<int:recording_id>                     download
 12375  GET              /health                                          health
 20520  GET              /healthz                                         healthz
 10721  GET              /login                                           dashboard_login_page
 10755  GET              /logout                                          dashboard_logout
 10762  GET              /manifest.webmanifest                            pwa_manifest
 21508  GET              /overlay                                         overlay_page
 10786  GET              /pwa-icon-<variant>.png                          pwa_icon
 10772  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (345)

```
   195  GET              /api/active-recordings                           api_active_recordings   [nc/routes/auskunft.py]
   422  GET              /api/activity-pulse                              api_activity_pulse   [nc/routes/auskunft.py]
   195  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   165  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
   993  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   738  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   864  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   844  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   882  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   806  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   356  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   367  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   377  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   400  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   407  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   418  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   546  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   644  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1231  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1263  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   341  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   946  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   926  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1099  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1147  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1198  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1057  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   901  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   504  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   768  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   650  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   633  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   625  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   456  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   472  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   812  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   374  GET              /api/archive/scan                                api_archive_scan   [nc/routes/archive.py]
   405  POST             /api/archive/scan/adopt                          api_archive_scan_adopt   [nc/routes/archive.py]
   777  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   797  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   684  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    49  GET/POST         /api/audio/config                                api_audio_config   [nc/routes/audio.py]
    78  POST             /api/audio/testtone                              api_audio_testtone   [nc/routes/audio.py]
   238  GET/POST         /api/auto-archive-rules                          api_archive_rules   [nc/routes/wartung.py]
   263  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete   [nc/routes/wartung.py]
   268  POST             /api/auto-archive-rules/run                      api_archive_rules_run   [nc/routes/wartung.py]
   163  GET              /api/azrael/agents                               api_azrael_agents   [nc/routes/azrael.py]
    99  POST             /api/azrael/ask                                  api_azrael_ask   [nc/routes/azrael.py]
   222  GET/POST         /api/azrael/context                              api_azrael_context   [nc/routes/azrael.py]
   120  GET              /api/azrael/core                                 api_azrael_core   [nc/routes/azrael.py]
   342  POST             /api/azrael/live_pause                           api_azrael_live_pause   [nc/routes/azrael.py]
   328  GET              /api/azrael/live_status                          api_azrael_live_status   [nc/routes/azrael.py]
   350  POST             /api/azrael/live_test                            api_azrael_live_test   [nc/routes/azrael.py]
   174  GET              /api/azrael/memories                             api_azrael_memories   [nc/routes/azrael.py]
   406  POST             /api/azrael/persona                              api_azrael_persona_set   [nc/routes/azrael.py]
   397  GET              /api/azrael/personas                             api_azrael_personas   [nc/routes/azrael.py]
   314  GET              /api/azrael/piper_status                         api_azrael_piper_status   [nc/routes/azrael.py]
   190  POST             /api/azrael/react                                api_azrael_react   [nc/routes/azrael.py]
   231  GET              /api/azrael/reaction                             api_azrael_reaction   [nc/routes/azrael.py]
   243  GET              /api/azrael/reactions                            api_azrael_reactions   [nc/routes/azrael.py]
   372  GET              /api/azrael/transcript                           api_azrael_transcript   [nc/routes/azrael.py]
   281  POST             /api/azrael/tts_test                             api_azrael_tts_test   [nc/routes/azrael.py]
   267  GET              /api/azrael/voices                               api_azrael_voices   [nc/routes/azrael.py]
   379  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model   [nc/routes/azrael.py]
   343  GET              /api/backoff-watch                               api_backoff_watch   [nc/routes/beobachtung.py]
   230  POST             /api/backup/run                                  api_backup_run   [nc/routes/wartung.py]
   196  GET              /api/backup/status                               api_backup_status   [nc/routes/wartung.py]
   179  POST             /api/backup/system                               api_backup_system   [nc/routes/wartung.py]
   399  GET              /api/bandwidth/live                              api_bandwidth_live   [nc/routes/auskunft.py]
   532  GET              /api/beobachtung/dienste                         api_beobachtung_dienste   [nc/routes/beobachtung.py]
   525  GET              /api/beobachtung/lage                            api_beobachtung_lage   [nc/routes/beobachtung.py]
   547  POST             /api/beobachtung/steuern                         api_beobachtung_steuern   [nc/routes/beobachtung.py]
   376  GET              /api/bookmarks                                   api_bookmarks_list   [nc/routes/auskunft.py]
   198  GET              /api/brain                                       api_brain   [nc/routes/brain.py]
   131  GET              /api/brain/alarms                                api_brain_alarms   [nc/routes/brain.py]
   116  GET              /api/brain/creator                               api_brain_creator   [nc/routes/brain.py]
    93  GET              /api/brain/graph                                 api_brain_graph   [nc/routes/brain.py]
   158  GET              /api/brain/growth                                api_brain_growth   [nc/routes/brain.py]
    80  GET              /api/brain/health                                api_brain_health   [nc/routes/brain.py]
    81  POST             /api/chat/send                                   api_chat_send   [nc/routes/chat.py]
    53  GET              /api/chat/send_status                            api_chat_send_status   [nc/routes/chat.py]
   174  GET              /api/checks                                      api_checks   [nc/routes/auskunft.py]
    40  GET              /api/cohost                                      api_cohost   [nc/routes/cohost.py]
    52  POST             /api/cohost/config                               api_cohost_config   [nc/routes/cohost.py]
    52  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    87  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   122  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   443  GET              /api/community/stats                             api_community_stats   [nc/routes/auskunft.py]
   433  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   418  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   238  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
   195  POST             /api/cookies/fetch                               api_cookies_fetch   [nc/routes/settings.py]
    73  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    80  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   497  GET              /api/data/export                                 api_data_export   [nc/routes/auskunft.py]
   259  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   286  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   379  POST             /api/db/restore/apply                            api_db_restore_apply   [nc/routes/settings.py]
   323  GET              /api/db/restore/list                             api_db_restore_list   [nc/routes/settings.py]
   341  POST             /api/db/restore/prepare                          api_db_restore_prepare   [nc/routes/settings.py]
   246  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
   164  GET              /api/defense/attacks                             api_defense_attacks   [nc/routes/abwehr.py]
   125  GET              /api/defense/crowdsec                            api_defense_crowdsec   [nc/routes/abwehr.py]
   146  GET              /api/defense/fail2ban                            api_defense_fail2ban   [nc/routes/abwehr.py]
    91  GET              /api/defense/overview                            api_defense_overview   [nc/routes/abwehr.py]
   244  POST             /api/discord/announce                            api_discord_announce   [nc/routes/discord.py]
   170  GET              /api/discord/clips_week                          api_discord_clips_week   [nc/routes/discord.py]
   188  GET              /api/discord/community                           api_discord_community   [nc/routes/discord.py]
   160  GET              /api/discord/invite                              api_discord_invite   [nc/routes/discord.py]
    63  GET              /api/discord/overview                            api_discord_overview   [nc/routes/discord.py]
   136  POST             /api/discord/webhook_test                        api_discord_webhook_test   [nc/routes/discord.py]
    79  POST             /api/donations/add                               api_donations_add   [nc/routes/money.py]
   112  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   120  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    60  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   136  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
    56  GET              /api/einstellungen                               api_einstellungen   [nc/routes/einstellungen.py]
    68  POST             /api/einstellungen                               api_einstellungen_setzen   [nc/routes/einstellungen.py]
   102  POST             /api/einstellungen/uebernehmen                   api_einstellungen_uebernehmen   [nc/routes/einstellungen.py]
    86  POST             /api/einstellungen/zuruecksetzen                 api_einstellungen_zuruecksetzen   [nc/routes/einstellungen.py]
   194  GET              /api/evolution/changelog                         api_evolution_changelog   [nc/routes/evolution.py]
   179  GET              /api/evolution/history                           api_evolution_history   [nc/routes/evolution.py]
    90  GET              /api/evolution/learned                           api_evolution_learned   [nc/routes/evolution.py]
   112  GET              /api/evolution/proposals                         api_evolution_proposals   [nc/routes/evolution.py]
   133  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss   [nc/routes/evolution.py]
   150  POST             /api/evolution/proposals/bulk                    api_evolution_bulk   [nc/routes/evolution.py]
    80  POST             /api/evolution/run                               api_evolution_run   [nc/routes/evolution.py]
   209  GET              /api/evolution/snapshots                         api_evolution_snapshots   [nc/routes/evolution.py]
    44  GET              /api/evolution/status                            api_evolution_status   [nc/routes/evolution.py]
   204  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   224  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   251  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
   394  GET              /api/forecast/storage                            api_forecast_storage   [nc/routes/auskunft.py]
   297  GET              /api/freeai/status                               api_freeai_status   [nc/routes/auskunft.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
   414  GET              /api/heatmap/lives/<username>                    api_heatmap_lives   [nc/routes/auskunft.py]
   409  GET              /api/heatmap/recordings                          api_heatmap_recordings   [nc/routes/auskunft.py]
   485  GET              /api/highlights                                  api_highlights   [nc/routes/auskunft.py]
    64  GET              /api/i18n/katalog                                api_i18n_katalog   [nc/routes/i18n.py]
    53  GET              /api/i18n/sprachen                               api_i18n_sprachen   [nc/routes/i18n.py]
   307  GET              /api/i18n/uebersetzer.js                         api_i18n_js   [nc/routes/i18n.py]
    77  POST             /api/i18n/waehlen                                api_i18n_waehlen   [nc/routes/i18n.py]
   168  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    43  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   150  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   125  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   189  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    76  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
    99  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   223  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
   222  GET              /api/kick/channel                                api_kick_channel   [nc/routes/kick.py]
   244  POST             /api/kick/channel                                api_kick_channel_set   [nc/routes/kick.py]
   103  GET              /api/kick/oauth/callback                         api_kick_oauth_callback   [nc/routes/kick.py]
   171  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect   [nc/routes/kick.py]
   149  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect   [nc/routes/kick.py]
    85  GET              /api/kick/oauth/start                            api_kick_oauth_start   [nc/routes/kick.py]
   128  GET              /api/kick/oauth/status                           api_kick_oauth_status   [nc/routes/kick.py]
   178  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck   [nc/routes/kick.py]
   119  POST             /api/kickmod/config                              api_kickmod_config   [nc/routes/kickmod.py]
   167  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords   [nc/routes/kickmod.py]
   184  GET              /api/kickmod/learned                             api_kickmod_learned   [nc/routes/kickmod.py]
   215  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear   [nc/routes/kickmod.py]
   191  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote   [nc/routes/kickmod.py]
   251  POST             /api/kickmod/say                                 api_kickmod_say   [nc/routes/kickmod.py]
   221  POST             /api/kickmod/start                               api_kickmod_start   [nc/routes/kickmod.py]
    82  GET              /api/kickmod/status                              api_kickmod_status   [nc/routes/kickmod.py]
   235  POST             /api/kickmod/stop                                api_kickmod_stop   [nc/routes/kickmod.py]
    66  GET              /api/lagebild                                    api_lagebild   [nc/routes/lagebild.py]
   428  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard   [nc/routes/auskunft.py]
    78  POST             /api/marketing/config                            api_marketing_config   [nc/routes/marketing.py]
   103  GET              /api/marketing/preview                           api_marketing_preview   [nc/routes/marketing.py]
   113  POST             /api/marketing/send-now                          api_marketing_send_now   [nc/routes/marketing.py]
    52  GET              /api/marketing/status                            api_marketing_status   [nc/routes/marketing.py]
    70  POST             /api/marketing/toggle                            api_marketing_toggle   [nc/routes/marketing.py]
   225  GET              /api/moderation/feed                             api_moderation_feed   [nc/routes/stats.py]
   100  POST             /api/news/config                                 api_news_config   [nc/routes/news.py]
    66  GET              /api/news/creators                               api_news_creators   [nc/routes/news.py]
    77  POST             /api/news/creators/generate                      api_news_creators_generate   [nc/routes/news.py]
   142  POST             /api/news/generate-now                           api_news_generate_now   [nc/routes/news.py]
   137  GET              /api/news/items                                  api_news_items   [nc/routes/news.py]
   128  GET              /api/news/preview                                api_news_preview   [nc/routes/news.py]
    53  GET              /api/news/status                                 api_news_status   [nc/routes/news.py]
    92  POST             /api/news/toggle                                 api_news_toggle   [nc/routes/news.py]
   257  GET              /api/ops/audit                                   api_ops_audit   [nc/routes/ops.py]
   324  GET              /api/ops/db-stats                                api_ops_db_stats   [nc/routes/ops.py]
   352  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown   [nc/routes/ops.py]
   203  GET              /api/ops/errors                                  api_ops_errors   [nc/routes/ops.py]
   270  GET              /api/ops/healthcheck                             api_ops_healthcheck   [nc/routes/ops.py]
   505  GET              /api/ops/log-tail                                api_ops_log_tail   [nc/routes/ops.py]
    80  GET              /api/ops/logtail                                 api_ops_logtail   [nc/routes/ops.py]
   168  GET              /api/ops/metrics                                 api_ops_metrics   [nc/routes/ops.py]
   151  GET              /api/ops/resource_history                        api_ops_resource_history   [nc/routes/ops.py]
   391  GET              /api/ops/version                                 api_ops_version   [nc/routes/ops.py]
   238  GET              /api/outcomes                                    api_outcomes   [nc/routes/auskunft.py]
   227  POST             /api/overlay/config                              api_overlay_config   [nc/routes/overlay.py]
   210  POST             /api/overlay/event                               api_overlay_event   [nc/routes/overlay.py]
   119  GET              /api/overlay/state                               api_overlay_state   [nc/routes/overlay.py]
   268  GET              /api/profile/<username>                          api_profile   [nc/routes/beobachtung.py]
   590  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk   [nc/routes/beobachtung.py]
   565  GET              /api/profile/snapshots/<username>                api_profile_snapshots   [nc/routes/beobachtung.py]
   308  GET              /api/public/stats                                api_public_stats   [nc/routes/auskunft.py]
   144  GET              /api/pulse                                       api_pulse   [nc/routes/auskunft.py]
   974  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
  1096  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
  1124  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
  1144  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   961  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
  1023  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
  1010  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   991  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   347  GET              /api/recording-attempts                          api_recording_attempts   [nc/routes/auskunft.py]
   636  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   631  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   679  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   562  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   889  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   653  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   616  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   589  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   863  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   733  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   822  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   728  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   661  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   441  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   906  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   529  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   784  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   939  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   924  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   485  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   723  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   709  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   692  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   749  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
  1287  GET              /api/recordings/session/<sid>                    api_recording_session   [nc/routes/recordings.py]
  1408  POST             /api/recordings/session/<sid>/join               api_recording_session_join   [nc/routes/recordings.py]
  1251  GET              /api/recordings/sessions                         api_recording_sessions   [nc/routes/recordings.py]
   842  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   738  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
   490  POST             /api/restream/<int:rid>/delete                   api_restream_delete   [nc/routes/restream.py]
   468  POST             /api/restream/<int:rid>/edit                     api_restream_edit   [nc/routes/restream.py]
   509  POST             /api/restream/<int:rid>/start                    api_restream_start   [nc/routes/restream.py]
   526  POST             /api/restream/<int:rid>/stop                     api_restream_stop   [nc/routes/restream.py]
   578  GET              /api/restream/chatfeed                           api_restream_chatfeed   [nc/routes/restream.py]
   444  POST             /api/restream/create                             api_restream_create   [nc/routes/restream.py]
   265  GET              /api/restream/deck                               api_restream_deck   [nc/routes/restream.py]
   165  GET              /api/restream/health                             api_restream_health   [nc/routes/restream.py]
   600  POST             /api/restream/layout                             api_restream_layout   [nc/routes/restream.py]
   413  GET              /api/restream/list                               api_restream_list   [nc/routes/restream.py]
   134  POST             /api/restream/report                             api_restream_report   [nc/routes/restream.py]
   539  POST             /api/restream/start_all                          api_restream_start_all   [nc/routes/restream.py]
   565  POST             /api/restream/stop_all                           api_restream_stop_all   [nc/routes/restream.py]
   191  GET              /api/restream/testpush                           api_testpush_status   [nc/routes/restream.py]
   216  POST             /api/restream/testpush                           api_testpush_run   [nc/routes/restream.py]
   388  GET              /api/restream/verify                             api_restream_verify   [nc/routes/restream.py]
   148  GET              /api/retention/preview                           api_retention_preview   [nc/routes/wartung.py]
   160  POST             /api/retention/run                               api_retention_run   [nc/routes/wartung.py]
   474  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   464  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   499  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
    65  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    86  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    52  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
   102  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   366  GET              /api/search                                      api_search   [nc/routes/auskunft.py]
    92  GET              /api/selftest                                    api_selftest   [nc/routes/selbsttest.py]
   456  GET              /api/shield/stats                                api_shield_stats   [nc/routes/auskunft.py]
   128  GET              /api/stats                                       api_stats   [nc/routes/stats.py]
   219  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern   [nc/routes/stats.py]
   214  GET              /api/stats/tiktok-status                         api_tiktok_status   [nc/routes/stats.py]
   274  GET              /api/stats/timeline                              api_stats_timeline   [nc/routes/stats.py]
   110  GET              /api/storage                                     api_storage   [nc/routes/wartung.py]
   116  POST             /api/storage/cleanup                             api_storage_cleanup   [nc/routes/wartung.py]
   578  GET              /api/stream/inspect/<username>                   api_stream_inspect   [nc/routes/beobachtung.py]
   397  GET              /api/stream/timeline                             api_stream_timeline   [nc/routes/beobachtung.py]
   427  GET              /api/stream/transcript                           api_stream_transcript   [nc/routes/beobachtung.py]
   126  GET              /api/streamer/compare                            api_streamer_compare   [nc/routes/streamer.py]
   273  POST             /api/streamer/delete/<username>                  api_streamer_delete   [nc/routes/streamer.py]
    88  GET              /api/streamer/detail                             api_streamer_detail   [nc/routes/streamer.py]
   298  GET              /api/streamer/digest/<username>                  api_streamer_digest   [nc/routes/streamer.py]
   230  GET              /api/streamer/dormant                            api_streamer_dormant   [nc/routes/streamer.py]
   254  GET              /api/streamer/exists/<username>                  api_streamer_exists   [nc/routes/streamer.py]
   185  GET              /api/streamer/journal/<username>                 api_streamer_journal   [nc/routes/streamer.py]
   150  GET/POST         /api/streamer/priority/<username>                api_streamer_priority   [nc/routes/streamer.py]
   210  GET              /api/streamer/watchlist                          api_streamer_watchlist   [nc/routes/streamer.py]
    56  GET              /api/streamers/wall                              api_streamers_wall   [nc/routes/streamer.py]
   219  GET              /api/summary/preview                             api_summary_preview   [nc/routes/auskunft.py]
    74  GET              /api/system                                      api_system   [nc/routes/systemlage.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
   178  GET              /api/system/check_timing                         api_check_timing   [nc/routes/systemlage.py]
   118  GET              /api/system/config_drift                         api_config_drift   [nc/routes/systemlage.py]
   141  GET              /api/system/config_snapshot                      api_system_config_snapshot   [nc/routes/systemlage.py]
   238  GET              /api/system/preflight                            api_system_preflight   [nc/routes/systemlage.py]
   105  GET              /api/system/preflight_history                    api_system_preflight_history   [nc/routes/systemlage.py]
   375  GET              /api/system/resilience                           api_system_resilience   [nc/routes/systemlage.py]
   389  GET              /api/tags                                        api_tags_list   [nc/routes/auskunft.py]
   189  GET              /api/top                                         api_top   [nc/routes/auskunft.py]
   237  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   458  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   487  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   407  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   420  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   516  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   393  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   268  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   313  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   337  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   324  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   164  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   282  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   133  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   374  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   429  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
   265  GET              /api/trend-7d                                    api_trend_7d   [nc/routes/auskunft.py]
   121  POST             /api/tunnel/set                                  api_tunnel_set   [nc/routes/ops.py]
   100  GET              /api/tunnel/status                               api_tunnel_status   [nc/routes/ops.py]
   132  POST             /api/tunnel/test                                 api_tunnel_test   [nc/routes/ops.py]
   113  POST             /api/tunnel/toggle                               api_tunnel_toggle   [nc/routes/ops.py]
   125  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback   [nc/routes/twitch.py]
    77  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect   [nc/routes/twitch.py]
   101  GET              /api/twitch/oauth/start                          api_twitch_oauth_start   [nc/routes/twitch.py]
    55  GET              /api/twitch/oauth/status                         api_twitch_oauth_status   [nc/routes/twitch.py]
   453  GET              /api/update/backups                              api_update_backups   [nc/routes/ops.py]
   419  GET              /api/update/check                                api_update_check   [nc/routes/ops.py]
   478  POST             /api/update/restart                              api_update_restart   [nc/routes/ops.py]
   458  POST             /api/update/rollback                             api_update_rollback   [nc/routes/ops.py]
   441  POST             /api/update/start                                api_update_start   [nc/routes/ops.py]
   434  GET              /api/update/status                               api_update_status   [nc/routes/ops.py]
   251  GET              /api/userstats                                   api_userstats   [nc/routes/auskunft.py]
   317  GET              /api/version                                     api_version   [nc/routes/auskunft.py]
    52  GET/POST         /api/webhooks                                    api_webhooks   [nc/routes/webhooks.py]
    92  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete   [nc/routes/webhooks.py]
   123  POST             /api/webhooks/<int:wid>/test                     api_webhook_test   [nc/routes/webhooks.py]
   107  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle   [nc/routes/webhooks.py]
   131  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback   [nc/routes/youtube.py]
   152  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget   [nc/routes/youtube.py]
   164  POST             /api/youtube/oauth/logout                        api_youtube_oauth_logout   [nc/routes/youtube.py]
    89  POST             /api/youtube/oauth/redirect                      api_youtube_oauth_redirect   [nc/routes/youtube.py]
   113  GET              /api/youtube/oauth/start                         api_youtube_oauth_start   [nc/routes/youtube.py]
    67  GET              /api/youtube/oauth/status                        api_youtube_oauth_status   [nc/routes/youtube.py]
   199  GET              /api/youtube/sendrate                            api_youtube_sendrate   [nc/routes/youtube.py]
    73  GET              /fonts/<name>                                    schrift   [nc/routes/schriften.py]
    66  GET              /fonts/schriften.css                             schriften_css   [nc/routes/schriften.py]
   469  GET              /metrics                                         api_prometheus_metrics   [nc/routes/beobachtung.py]
```

## Discord-Slash-Commands in discordbot.py (67)

```
  2256  /about                  Ueber diesen Bot
   961  /ai                     
  2256  /aireset                KI-Kontext zuruecksetzen
  1375  /ask                    
  1062  /assign_role            
  1112  /ban                    
  2211  /botstats               
  2256  /brain                  Brain-Lage: Regeln, Agenten, Empfehlungen
  2256  /bulkadd                Mehrere User auf einmal tracken · a b c
  2256  /cleanup                Alte Aufnahmen aufraeumen
  1641  /clearwarns             
  2175  /clip                   
  2160  /clipoftheweek          
  1511  /clips                  
  2256  /cookies                Cookie-Status — mit 'holen' selbst beziehen · [holen]
  1017  /create_category        
   988  /create_channel         
  1052  /create_group           
  1027  /create_role            
  1003  /create_voice           
  1253  /daily                  
  2256  /diag                   Vollstaendige Diagnose
  2256  /einnahmen              Einnahmen und Spenden
  1404  /event                  
  1446  /events                 
  1551  /follow                 
  1540  /help                   
  1102  /kick                   
  1228  /leaderboard            
  2256  /live                   Live-Status sofort pruefen · @user
  1498  /livenow                
  2256  /logs                   Letzte Fehler aus dem Log
  2256  /pause                  Tracking pausieren · @user
  1526  /post_test              
  1336  /profile                
  1134  /purge                  
  2256  /quelle                 Stream-Quellen eines Live-Nutzers messen (alle Wege, ffprobe
  2256  /quota                  Speicher-Quota
  1215  /rank                   
  1486  /recstatus              
  1072  /remove_role            
  2256  /report                 Azrael-Sentinel-Wochenreport
   974  /restream_status        
  2256  /resume                 Tracking fortsetzen · @user
  1082  /set_channel_perms      
  1177  /setup_community        
  1194  /setup_targets          
  1472  /spenden                
  1583  /stats                  
   933  /status                 
  2256  /stoprec                Laufende Aufnahme sauber beenden · @user
  1679  /streaminfo             
  2256  /summary                Tageszusammenfassung
  2256  /sysres                 System-Ressourcen
  2256  /teststream             Recorder-Selbsttest · @user
  2256  /tiktok                 Profil-Analyse eines TikTok-Accounts · ‹name›
  1122  /timeout                
  1651  /topstreamers           
  2256  /topusers               Top-Streamer nach Aufnahmen
   863  /track                  
  2256  /track_exact            Exakten Usernamen tracken (ohne Korrektur) · ‹name›
   946  /tracklist              
  1565  /unfollow               
  2256  /unpause                Auto-pausierte Quelle wieder aktivieren · @user
   895  /untrack                
  1604  /warn                   
  1627  /warnings               
```

## Discord-Events in discordbot.py (4)

```
  2419  on_member_join
  2376  on_message
  2277  on_raw_reaction_add
  2454  on_ready
```

## Top-Level-Symbole in telegramversand.py (2 Funktionen)

```
    58-73     konfiguriere
    76-490    split_and_send_video
```

## Top-Level-Symbole in discordbot.py (54 Funktionen)

```
  1756-1807   _award_xp
   535-562    _bereich_umziehen
   482-492    _clip_kopieren
  1978-2007   _clip_week_leader
  2031-2045   _clipoftheweek_loop
  2571-2633   _community_events_loop
  1713-1735   _dc_client
  1738-1747   _dc_offen
  2673-2708   _disc_automod_check
   408-413    _disc_sprache_setzen
  1810-1858   _discord_ai_automod
   684-723    _discord_automod
  1861-1881   _discord_azrael_reply
  2048-2530   _discord_run_once
   243-301    _discord_start
   304-358    _ensure_discord_invite
  2536-2568   _ensure_error_channel
   429-442    _ensure_rank_roles
   826-840    _ensure_team_roles
  2636-2666   _error_channel_loop
   733-737    _guard
   653-681    _handle_voice_ai
   416-426    _is_admin
   507-532    _link_video
  1926-1937   _liveboard_loop
   740-758    _on_level_up
   649-650    _par_chat_id
  2010-2028   _post_clip_of_week
  1940-1958   _post_weekly_digest
   445-471    _provision_base_channels
  1478-1572   _reg_betrieb
  1148-1242   _reg_community_setup
  1245-1325   _reg_daily_profil
  1368-1465   _reg_frage_events
   920-976    _reg_info
  1094-1145   _reg_moderation
  1328-1365   _reg_profil
  1043-1091   _reg_rollen
   979-1040   _reg_server
  1468-1475   _reg_spenden
  1575-1662   _reg_streamer
  1665-1710   _reg_system
   854-917    _reg_tracking
   793-823    _run_tg_handler
   636-646    _tracked_usernames
   160-222    _uebernehmen
   495-504    _umzugsmarken
  1890-1923   _update_liveboard
  1961-1975   _weekly_digest_loop
   474-479    _ziel_guild
   565-607    _ziele_abgleichen
   616-633    _ziele_sync_loop
   610-613    _ziele_takt_min
   225-228    starte
```

## Top-Level-Symbole in bot.py (580 Funktionen, 4 Klassen)

```
 26542-26564  _abbruch_datenbank_unlesbar
  2761-2762   _abo_key
  2782-2800   _abo_probe_dump
 26660-26676  _abschied_wachen
 26679-26697  _abschluss
 16810-16817  _ad_allowlist
 17972-17978  _agent_for
 17981-17997  _ai_telemetry
 18494-18512  _alert
 22403-22453  _alert_monitor_loop
 19173-19230  _alte_beilagen_einsammeln
 22835-22897  _announce_loop
  3661-3671   _anthropic_key
  3678-3680   _anthropic_model
 10385-10388  _arg_int
  2753-2758   _as_dict
 26228-26237  _async_exc_handler
 18675-18697  _audio_tap_cmd
 19686-19745  _audio_tap_melden
 18711-18735  _audio_tap_sammler
  9730-9767   _aufnahme_beim_stopp_sichern
 19115-19136  _aufnahme_chat_ausklang
 19099-19112  _aufnahme_chat_beginnen
 19258-19279  _aufnahme_chat_dienst
 19452-19505  _aufnahme_chat_einarbeiten
 19094-19096  _aufnahme_chat_modus
 19282-19331  _aufnahme_chat_nachtrag
 19139-19170  _aufnahme_chat_vormerken
 19249-19255  _aufnahme_chat_wecken
 25475-25477  _aufnahme_deckel
 19334-19355  _aufnahme_fertigmachen
  9770-9788   _aufnahme_platz_frei
 26624-26644  _aufnahmen_abschliessen
 26567-26621  _aufraeumen
 10584-10653  _auth_cookie
 10542-10580  _auth_guard
  1988-1993   _auto_on
 20372-20390  _auto_restream_loop
 14432-14474  _avatar_frames_laden
 16860-16873  _azrael_brain_kontext
 23975-23990  _azrael_broadcast_reply
 23875-23897  _azrael_chat_reply
 23847-23872  _azrael_chat_should_reply
 23903-23905  _azrael_gate_cfg
 18002-18016  _azrael_live_state
 21421-21435  _azrael_overlay_state
 18376-18430  _azrael_proactive_loop
 17820-17876  _azrael_reaction_to_chats
 23908-23915  _azrael_reply_all_chats
 23834-23844  _azrael_self_names
 23943-23972  _azrael_send_to
 14393-14429  _azrael_spricht
 14736-14749  _azrael_stimme_stumm
 18022-18043  _azrael_system
 22537-22540  _backup_active
 22618-22631  _backup_loop
 25564-25568  _betrieb
 26301-26310  _brain_crowdsec_snap
 26469-26472  _brain_db_health
 22324-22333  _brain_growth_loop
 10979-11006  _brain_growth_snapshot
  2672-2706   _brain_hint_delay
 26373-26408  _brain_moderation_snap
  6662-6690   _brain_notify
 26475-26497  _brain_recording_snap
 26313-26370  _brain_restream_health
 26500-26513  _brain_tiktok_status_snap
 12280-12297  _browser_push
  6702-6789   _build_daily_summary
 14783-14787  _build_restream_cmd
  5415-5442   _can_stop_tracking
  2101-2123   _capture_set_cookies
 12965-12968  _cfg_get
 12971-12973  _cfg_set
 21146-21181  _channel_set_all
 13544-13547  _chat_connected
 13550-13566  _chat_disconnected
 19243-19246  _chat_einarbeiten_async
  9245-9256   _chat_is_forum
 19063-19088  _chat_listener_abbauen
 13586-13588  _chat_sanitize
 13529-13541  _chat_stat
 13569-13572  _chat_stats_snapshot
  3984-3996   _check_ai_models_sync
 11261-11304  _classify_pool_anonymity
 11307-11324  _classify_pool_anonymity_bg
   904-926    _claude_chat_sync_metered
 10417-10423  _client_ip
 23474-23488  _clip_chat_ass
 22981-23015  _clip_prune
 23018-23028  _clip_recfile_for
 23394-23462  _clip_schneiden
 23491-23497  _clip_should_velocity
 23072-23157  _clip_to_discord
 19423-19428  _clips_abwarten
  3865-3874   _close_ai_session
 24021-24036  _cohost_broadcast
 24006-24007  _cohost_cfg
 24062-24074  _cohost_fire_highlight
 24010-24018  _cohost_gate
 24039-24059  _cohost_highlight
 10909-10911  _conv_messages
  7086-7147   _cookie_alarm_loop
  2191-2192   _cookie_autofetch_info
  2175-2179   _cookie_autorefresh_info
 25935-25957  _cookie_bezug_loop
 25960-25985  _cookie_bezug_runde
  2078-2082   _cookie_header
 10426-10431  _cookie_sicher
  2204-2218   _cookies_selbst_holen
  4205-4207   _create_index_safe
 21867-21981  _crowdsec_status
 21813-21864  _crowdsec_via_lapi
 21717-21735  _cscli_bin
 21744-21757  _cscli_path
  6970-6997   _daily_summary_loop
 21775-21792  _darf_journal_lesen
  3186-3211   _darf_ytdlp_nachschlagen
 12461-12482  _dashboard_adresse
  1486-1516   _dashboard_trackings_umziehen
 23465-23471  _datei_weg
 22377-22400  _db_maintenance_loop
  6920-6967   _db_vacuum_loop
 16833-16857  _detect_foreign_ad
  1668-1679   _diag_path_owner
 18281-18326  _director_finalize
 19675-19682  _director_for
 18230-18278  _director_mark
 23307-23310  _disc_state_get
 23313-23320  _disc_state_set
 22305-22314  _discord_bot_starten
 22268-22279  _discord_einladung_merken
 22317-22321  _discord_invite
 22282-22302  _discord_kontext
 23268-23304  _discord_live_thread
 18433-18445  _discord_notify
 22240-22265  _discord_ops_alert
 23168-23264  _discord_post_user
 22900-22906  _discord_stop
  7000-7081   _disk_alarm_loop
 25858-25909  _disk_autoclean
 26083-26096  _disk_guard_loop
 14371-14378  _drossel_hoeher
 14367-14368  _drossel_stufe
 14381-14389  _drossel_zuruecksetzen
 12638-12640  _dump_all_threads
 25571-25585  _einstellungen_startzeile
 11187-11250  _enrich_proxies_with_geo
  2247-2308   _ensure_cookie_file_netscape
  9418-9421   _ensure_notify_topic
 11431-11468  _ensure_proxy_ready
  9272-9294   _ensure_topic
   745-747    _env_int
   750-752    _env_int_range
 18478-18491  _event_webhook
 13312-13325  _evolution_loop
  6104-6138   _extract_file_payload
  2380-2382   _extract_urls_from_streamurl_node
 21760-21767  _f2b_sudo_hint
  1472-1483   _fanout_ziele
 26700-26763  _fatal_vom_botteil
 25480-25495  _fd_grenze_anheben
  4879-4889   _fehler_text
 11088-11106  _fetch_proxy_list
 19032-19060  _fetch_tiktok_room_id
   830-833    _ff_cmd
 19436-19449  _ffprobe_masse
 14150-14155  _find_chromium
  3581-3583   _find_external_recorder
  2385-2387   _find_stream_urls
 13016-13041  _fire_webhooks
  7965-7974   _fork_safe
   937-950    _freeai_chat_sync_metered
 21806-21810  _geo_lookup_ips
  3853-3862   _get_ai_session
  7798-7838   _get_live_info
  3037-3044   _get_resolve_semaphore
  8445-8865   _handle_single_tracking
 25680-25682  _hb
 25685-25702  _hb_while
 13600-13602  _highlight_cfg
 13605-13634  _highlight_observe
 14201-14209  _htmlov_bild_schreiben
 14179-14198  _htmlov_dauerbrowser
 14158-14176  _htmlov_screenshot_cmd
 18737-18747  _httpx_proxy
 13049-13061  _in_quiet_hours
 26528-26539  _init_db_oder_abbruch
 27347-27378  _install_fast_eventloop
 10280-10334  _install_fast_json
 12643-12659  _install_faulthandler
 20423-20432  _intel_ensure_schema
 20475-20510  _intel_index_loop
 20444-20459  _intel_index_one
 20435-20441  _intel_semantic
  5404-5413   _is_authorized
  8317-8338   _is_dead
  2370-2372   _is_hevc
 21795-21797  _is_private_ip
  1887-1894   _is_process_running
  6692-6699   _is_quiet_hours
  1391-1400   _is_upload_window
  4744-4759   _iso
 10434-10440  _ist_lokal
 10369-10382  _json_error_handler
  6914-6915   _kick_broadcaster_id
  8192-8199   _kick_cluster_gefunden
  8127-8189   _kick_cluster_weiter
  6826-6868   _kick_follower_count
  6810-6813   _kick_slug
 12093-12100  _kick_user_token
  8097-8124   _kick_ws_pause
 26516-26525  _kickmod_boot
  4289-4292   _kind_from_filename
 13078-13080  _latest_popularity
  1824-1833   _laufstand
 26043-26080  _laufstand_loop
 25604-25642  _leistung_erheben
  7672-7699   _link_video_senden
 20081-20130  _live_react_loop
 19748-20070  _live_react_worker
  3429-3543   _live_status_aufloesen
 17879-17890  _live_transcript_push
 20072-20079  _live_users
 18329-18373  _living_title_loop
 22543-22615  _local_backup_scan
  4684-4707   _lock_update
 10351-10365  _log_5xx
 25645-25677  _log_schleuse_pruefen
   820-827    _log_sicher
 14795-14807  _looks_like_codec_err
 14790-14792  _looks_like_source_expired
  8015-8045   _loop_fehler
 12663-12672  _loop_heartbeat
 25386-25419  _loop_lag_monitor
 25433-25453  _loop_stockung_melden
 25456-25466  _loop_takt_starten
 12675-12748  _loop_watchdog_thread
 17756-17773  _loyalty_add
 17747-17753  _loyalty_get
 17776-17784  _loyalty_top
  5086-5105   _manual_status
  8340-8341   _mark_dead
 11707-11723  _marketing_loop
 23922-23940  _maybe_handle_command
 26182-26206  _maybe_hype_clip
 22950-22978  _meme_klassifizieren
 19358-19420  _meme_zusammenschnitt
  4192-4197   _migrate_columns
 24204-24215  _mod_is_exempt
 24218-24223  _mod_warn_first
 24226-24229  _mod_warn_text
 13369-13388  _modlog
 13352-13366  _modlog_schreiben
  1087-1089   _multistream_targets
  3214-3250   _nachschlag_ytdlp
  7977-7978   _nc_create_subprocess_exec
  7981-7982   _nc_create_subprocess_shell
 12030-12047  _news_loop
 13411-13413  _normalize_ingest
  2603-2620   _note_check_duration
  9412-9415   _notify_topic_name
  2807-2813   _offline_ergebnis
  3253-3276   _ohne_url_melden
 17905-17913  _oracle_memories
 18179-18213  _oracle_memorize
 17916-17929  _oracle_persona
 17898-17902  _oracle_recent_text
 13789-13790  _ov_atomic_write
 13780-13782  _ov_bar
 16736-16748  _ov_clip_text
 13785-13786  _ov_oneline
 21472-21501  _overlay_push
 14104-14147  _overlay_render_size
 13480-13484  _overlay_session_reset
 21437-21439  _overlay_src_ok
 16820-16830  _own_invites
 14099-14101  _parse_size
 21989-22069  _parse_ssh_attacks
  7348-7381   _pause_resume_cmd
  2129-2173   _persist_refreshed_cookies
  2032-2064   _pick_checked_pull_proxy
 10471-10484  _pin_auth_value
 10531-10532  _pin_clear_fail
 10511-10514  _pin_locked
 10517-10528  _pin_note_fail
 10487-10508  _pin_ok
 21279-21304  _piper_pick_model
 21364-21415  _piper_say
 12978-13013  _post_json_threaded
 14078-14096  _probe_video_size
  1915-1932   _proc_is_recorder
 11400-11428  _proxy_pool_refresh_loop
  1998-2029   _proxy_report_recording
  9004-9077   _pruef_runde
  8963-9001   _pruefstand_melden
 25515-25526  _pruefung_verworfen
 12628-12630  _prune_stall_dumps
 11777-11949  _public_stats
  2195-2201   _pull_proxy_still
 18449-18475  _push_notify
 10700-10702  _pwa_dir
 11157-11172  _quick_validate_proxy
 13044-13046  _quiet_hours_config
 10665-10698  _rate_guard
 17717-17723  _react_warn
  7885-7924   _reap_proc
  9660-9727   _rec_auto_abschalten
  9607-9657   _rec_frueh_getrennt
  9476-9552   _rec_kategorie_melden
  9555-9604   _rec_totstreak_fortschreiben
  2643-2665   _record_check_outcome
   815-817    _redact_stream_urls
 11327-11397  _refresh_proxy_pool
  2420-2511   _resolve_via_html
  2816-3014   _resolve_via_webcast_api_v2
  3077-3162   _resolve_via_ytdlp
 23531-23660  _resolve_youtube_ingest
  2396-2417   _resolver_stumm
 13463-13474  _restream_active_sources
 14477-14601  _restream_avatar_feeder_start
 14604-14613  _restream_avatar_feeder_stop
 19508-19639  _restream_chat_guardian
 13637-13709  _restream_chat_push
 13766-13775  _restream_chat_push_async
 26411-26466  _restream_durchreicher
 14212-14334  _restream_html_overlay_start
 14337-14354  _restream_html_overlay_stop
 13422-13445  _restream_overlay_files
 20134-20166  _restream_platform_state
 20334-20369  _restream_resume_after_restart
 13740-13763  _restream_status_schreiben
 14661-14733  _restream_tts_enqueue_wav
 14040-14072  _restream_tts_feeder
 14037-14038  _restream_tts_fifo_path
 14616-14643  _restream_tts_start
 14645-14659  _restream_tts_stop
 20172-20331  _restream_verify_loop
 22508-22520  _retention_loop
 22502-22505  _retention_scan
  2764-2766   _room_is_abo
  6142-6259   _run_ai_call
 12771-12784  _run_async_from_flask
 21800-21803  _run_priv
 27335-27343  _run_selfcheck_and_exit
 22523-22534  _s3_client
  8367-8418   _safe_send
  5012-5028   _sample_net_throughput
  2709-2739   _schedule_next_check
 22456-22499  _scheduler_loop
  4200-4202   _schema_pk
 12788-12793  _scraper_session
 24232-24271  _screen_full
 12144-12181  _sec_headers
  2375-2377   _select_stream_from_data_section
 27055-27332  _selfcheck
  9424-9458   _send_live_notice
  1414-1418   _should_defer_upload
 23031-23069  _shrink_for_discord
 10705-10717  _sicheres_ziel
 22336-22374  _sicherheits_erinnerung_loop
 26103-26120  _sign_health_check
 26123-26142  _sign_health_loop
  4762-4787   _sitzung_bestimmen
  7994-8005   _spawn
 27766-27796  _spawn_from_flask
 25529-25535  _speicher_maps
 25538-25553  _speicher_pflegen
 18749-19029  _start_chat_listener
 25498-25512  _start_gesperrt
 12751-12768  _start_loop_watchdog
 11976-12025  _stats_loop
 11955-11958  _stats_output_path
 11961-11973  _stats_write
 21316-21330  _stimme_saubern
 21337-21361  _stimme_schon_gesagt
  8944-8960   _storage_cleanup_loop
 26162-26169  _story_for
  3606-3612   _stream_url_expiry
  3614-3619   _stream_url_ttl
 16783-16790  _streamer_persona_get
 22640-22792  _system_backup
 22801-22831  _system_backup_loop
 12588-12606  _task_auf_bot_schleife
 25069-25085  _telegram_befehlsmenue
  8048-8094   _telegram_polling_fehler
  1452-1469   _telegram_ziele
 11109-11148  _test_proxy
 11655-11671  _testpush_resolve_live
 19431-19433  _text_schreiben
  8343-8364   _tg_sprache_setzen
  9346-9399   _tg_topic_umziehen
  9316-9343   _tg_topic_umzug
  9212-9222   _tg_topics_load_into_mem
  9209-9210   _tg_topics_path
  9224-9231   _tg_topics_save
 10443-10453  _token_ok
  9297-9313   _topic_anlegen
  9234-9243   _topic_forget
 13064-13075  _tracking_max_duration
  4497-4511   _tracking_remove_cleanup
  4528-4540   _tracking_resume_cleanup
  1726-1749   _try_attach_file_handler
 21306-21314  _tts_cleanup
 11631-11635  _tunnel_effective
 25912-25932  _tunnel_lage
 25988-26040  _tunnel_wacht_loop
 20805-20858  _twitch_channel_status
 24274-24422  _twitch_chat_loop
 23326-23339  _twitch_clip_versuchen
 24085-24191  _twitch_eventsub_loop
  1437-1450   _upload_queue_add
  1528-1530   _upload_queue_count
  1420-1429   _upload_queue_load
  1410-1412   _upload_queue_path
  1519-1526   _upload_queue_remove
  1431-1435   _upload_queue_save
  9267-9269   _upload_topic_name
  1532-1576   _upload_window_loop
  7858-7865   _uptime_s
 13399-13408  _url_host
  3279-3377   _url_nachschlag
   897-901    _usage_record_claude
 26276-26298  _v37_pause_source
 26240-26250  _v37_restream_restart
 26253-26273  _v37_unpause_source
  8266-8310   _verbindung_verloren
  6871-6902   _viewer_sample_loop
 10535-10538  _wants_html
  7868-7882   _warn_empty_env
 25723-25844  _watchdog_loop
 23806-23814  _wchat_thank_ok
 18517-18547  _whisper_get_model
  7955-7962   _whisper_native_section
 17704-17710  _whisper_pool
 18641-18673  _whisper_segments
 18549-18565  _whisper_stumm
 18568-18638  _whisper_transcribe
 13837-13994  _write_restream_overlay
 13799-13834  _write_restream_overlay_async
 24446-24545  _youtube_api_chat_loop
 20861-20964  _youtube_api_status
 20967-21034  _youtube_channel_status
 24548-24712  _youtube_chat_loop
 23342-23367  _youtube_clip_versuchen
 23666-23679  _youtube_restream_autoconfig
 23682-23706  _youtube_restream_autoconfig_inner
 23773-23801  _youtube_send
 21102-21143  _youtube_set_channel
 23709-23743  _yt_access_token
 23746-23761  _yt_live_chat_id
 23769-23770  _yt_sendrate_cfg
 24425-24440  _yt_timeout
  3061-3062   _ytdlp_detect_available
  3064-3075   _ytdlp_note_result
 12633-12635  _zombie_child_count
 25588-25601  _zustand_kennzahlen
  7734-7758   about
  4408-4412   add_ai_log_entry
  4325-4328   add_archive_entry
  5050-5052   add_archive_rule
  4790-4861   add_recording
  4472-4489   add_tracking
  6262-6295   ai
  4010-4096   ai_chat
  4130-4140   ai_history_append
  4142-4147   ai_history_clear
  4119-4128   ai_history_load
  4104-4117   ai_rate_limit_check
  6324-6332   aireset
 18046-18065  azrael_chat
 24717-24839  brain_cmd
  3622-3627   build_recording_cmd
  4492-4495   bulk_add_trackings
  7150-7209   bulkadd
  9080-9192   check_all_trackings
  4544-4556   claim_live_transition
 16876-17636  class KickModerator
 14810-16623  class RestreamManager
  4710-4711   class _AufnahmeLockVerloren
  8202-8263   class _KickClusterSuche
 11514-11556  classify_proxy_anonymity
  6370-6568   cleanup
  5340-5346   cleanup_old_recordings
  4735-4742   clear_recording
 23370-23391  clip_moment
  5002-5005   compute_storage_forecast
  7272-7345   cookies_cmd
  4463-4469   count_trackings_for_chat
  4395-4406   decide_preferred_recorder
  4335-4338   delete_archive_entry
  5054-5056   delete_archive_rule
  5799-5946   diag
 24951-25012  einnahmen_cmd
  4996-4999   find_recordings_by_fingerprint
  4356-4372   finish_recording_attempt
  4516-4518   get_all_active_trackings
  4423-4425   get_all_checks
  4863-4866   get_all_recordings
  4945-4947   get_all_tags_with_counts
  4973-4976   get_annotations_for_recording
  4330-4333   get_archive_entry
  4966-4969   get_bookmarked_recordings
  2235-2240   get_cookie_health
  4933-4939   get_event_log
  4379-4393   get_last_recording_attempt
  3380-3422   get_live_status
  5279-5282   get_manual_recordings
  4981-4984   get_or_compute_inspect_sync
  5381-5384   get_outcome_breakdown
  4952-4955   get_priority_poll_interval
  4374-4377   get_recent_recording_attempts
  4868-4871   get_recording_by_id
  4959-4962   get_recording_note
  3793-3822   get_redis
  4452-4455   get_stats
  5334-5338   get_storage_stats
  5074-5076   get_tiktok_status_distribution
  4558-4567   get_tracking_state
  4513-4514   get_trackings_for_group
  5295-5298   get_trash_recordings
  9791-10259  handle_recording_finished
 25061-25066  hilfe_cmd
  4215-4280   init_db
  5046-5048   list_archive_rules
  5584-5622   live
  8421-8443   live_check_worker
  3877-3920   llm_chat
  3943-3974   llm_chat_sync
  3928-3940   llm_list_models
  4892-4925   log_event
  1849-1882   log_recording_failure
  7495-7544   logs_cmd
 26766-27045  main
  6298-6321   on_ai_media
  7621-7647   on_ai_reply
  7702-7731   on_azrael_mention
  7763-7793   on_callback
  7656-7669   on_link_video
 18071-18176  oracle_handle
  7384-7387   pause_tracking
  5394-5399   profile_keyboard
  5537-5581   quelle
  7446-7492   quota
  8867-8941   reaper_loop
  5070-5072   record_tiktok_status
  6337-6367   recstatus
  3824-3832   redis_get_json
  3835-3841   redis_set_json
 25088-25098  report_cmd
 11559-11561  report_proxy_result
  2514-2556   resolve_tiktok_live_stream
  5290-5293   restore_recording
  7390-7393   resume_tracking
  5059-5064   run_archive_rules
 25101-25366  run_bot
 12485-12579  run_flask
  5034-5037   sample_bandwidth_for_active
  4415-4421   save_tiktok_check
  4714-4733   set_recording_file
  4521-4525   set_tracking_paused
  5285-5288   soft_delete_recording
 25046-25058  spenden_cmd
  9464-9474   split_and_send_video
  5447-5489   start
  4340-4354   start_recording_attempt
  6571-6609   stats
  5224-5277   stop_manual_recording
  7396-7443   stoprec
  6795-6803   summary_cmd
  7547-7618   sysres
  5948-6092   teststream
  5491-5532   tiktok
  7212-7269   topusers
  5659-5716   track
  5624-5656   track_exact
  5730-5797   tracklist
  5108-5222   trigger_manual_recording
  4646-4681   try_acquire_recording_lock
  5301-5303   universal_search
 25015-25043  unpause_cmd
  5718-5728   untrack
 24842-24948  update_cmd
  4991-4994   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, class BestandUnbekannt, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, finde_ohne_eintrag, get_archive_entries_paged, get_archive_entry, run_archive_file_check, uebernehmen
archivename.py         open_unique
archiverules.py        add_archive_rule, delete_archive_rule, list_archive_rules, run_archive_rules
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
audiocue.py            config, configure
audiotap.py            diagnose, melden, warum_kein_tap
aufnahmechat.py        ass, ausschnitt, beenden, beginnen, clip_beginnt, clip_fertig, clip_merken, clips_nehmen, clips_offen, concat_liste, einbrennen_cmd, laeuft, modus, notieren, untertitel_cmd, zusammenschnitt_cmd
aufnahmefolge.py       aufnahme_geglueckt, daten_geflossen, melden_erlaubt, nach_403, nach_frueher_trennung, nach_totem_versuch, sitzung_zuende, sperre_rest, stall_grenze
aufnahmekategorie.py   kategorisiere
aufnahmesitzung.py     abdeckung, angleich_cmd, braucht_angleich, concat_cmd, concat_liste, gehoert_dazu, luecken, probe_cmd, sekunden, sitzung_id, tonformat, zieldatei
auslieferung.py        schreibe, stand, text
avatarloop.py          blinzeln, ruhe_seit, schleife, zustand
azraelkontext.py       ausfall, block, fakten, letzte_erinnerung, nachricht, restream_quellen, sicher, streamer_waehlen
azraelstate.py         configure, flag, haken, personas_load, personas_path, personas_save
backupcfg.py           aktiv, fehlgrund, lokal, lokal_dir, recordings_retain_days, retention_days, s3, s3_bucket, s3_endpoint, s3_konfiguriert, s3_region, s3_zugang, sys_backup, sys_hour, sys_keep, sys_max_file_mb
badwords.py            banned_path, configure, fetch_ldnoobw_de, learned_path, load_banned, load_learned, save_banned, save_learned
bandbreite.py          messen
befehle.py             beschreibung, discord_nativ, discord_ueber_tg, fuer, hilfe_text, pruefen, telegram_handler
beobachtungsdienst.py  fuer_deck, grafana_jetzt, grafana_lage, grafana_unit, grund_text, installiert, prometheus_jetzt, prometheus_lage, selbstheilung_erlaubt, steuern
beobachtungslage.py    grafana, lage, prometheus
betriebslage.py        abschiedswache, bereit, bewerten, haengende_threads, sichern_beim_stopp
binresolve.py          resolve
botctx.py              class BotKontext
brainstate.py          history_for, record, stall, stream_recent
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat, restream_active, yt_sendrate_cfg
chatfolge.py           entscheide
chatnachtrag.py        beilage_lesen, beilage_zu, eingearbeitet, ensure_schema, erledigt, fehlversuch, ist_beilage, lesen, offene, stempel, unveraendert, vormerken
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, fehlertext, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
clientip.py            echte_ip, ist_https, ist_lokal
cohost.py              config, decide, default_config, new_state, prompt_seed, snapshot
community.py           anzeigename, configure, darf_pingen, highlight_post, highlight_share_enabled, live_ping, live_ping_enabled, note_chatter, returning_enabled, rollen_id, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookiebezug.py         anstossen, configure, faellig, gast_hilft, holen, info, intervall_s, naechster_lauf
cookieholen.py         aktualisiere, aus_browser, configure, hole_gastcookies, schreibe, zusammenfuehren
cookies.py             configure, gesundheit, lade_jar, load_dict
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, erwartete_namen, fehlende_namen, gesetzte, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dashauth.py            erlaubt_offen, geschuetzt, host, lage, nur_lokal, offen_im_netz, zurueckgefallen
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbgesundheit.py        messen
dbrestore.py           archive, dump_aus_archiv, einsetzen, einspielen, vorbereiten
dbwartung.py           faellig_in, letzter_lauf, merken, stand_datei
dbwrap.py              class DatenbankUnlesbar, configure_db, datei_diagnose, db_async, db_conn, get_pool, set_pool
ddlsafe.py             ddl, ist_schon_da
defensecfg.py          bouncer_gesetzt, bouncer_key, geo_fehler, geo_fehler_setzen, lapi_host, lapi_port, lapi_url, server_lat, server_lon
director.py            class LiveDirector, configure
discordlimits.py       aktuell_label, aktuell_mb, configure, describe, effective_upload_mb, gate_mb, guild_filesize_bytes, guild_limit_mb
discordrang.py         rang_fuer_level, slug, xp_fuer_level, xp_zu_level
discordstate.py        invite, state_get
discordziele.py        clip_kanal, clip_kanal_des_bereichs, clip_kanal_holen, eigene_kanaele, loeschbar, umzugsmarke, umzugsmarke_lesen
donations.py           configure, fmt_eur, parse_number, source_allowed, to_eur, unknown_count
donationsdb.py         manual_rows, manual_total, parse_eur
durchreicher.py        adresse, ist, main, nutzer_aus, werkzeug, werkzeuge, zieher_cmd, zieher_umgebung, zubringer_cmd
einstellungen.py       class Abgelehnt, db_werte, geheim, gueltiger_name, in_umgebung_laden, katalog, pruefen, schutzgrund, setzen, startbericht, uebernehmen, uebersicht, zuruecksetzen
encodeschlange.py      lage, last_frei, parallel, platz, platz_sync
envdatei.py            class EnvdateiFehler, lesen, main, setzen, wert_lesen, wert_schreiben
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventlog.py            leeren, schreibe, stand
eventquery.py          build_query
evolution.py           analyze, build_dir, conf, configure, cycle, engineering_note, next_version, write_build
fehlertext.py          nach_aussen, saeubern
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      anzeige_groesse, avatar_kette, chat_umbruch_w, chat_zeilen, drawtext_chain, studio_chain, studio_masse
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, dienstmeldung, katalog_kennt, last_errors, list_models_sync, stream_haeppchen, stream_rest
gegendruck.py          abgewiesen, deckel_auto, fd_grenze_anheben, fd_lage, freigeben, lage, reservieren, reserviert, start_entscheiden, verworfen, zuruecksetzen
geocache.py            get, groesse, leeren, put
geoip.py               ist_privat, lookup
geschuetzt.py          lage, ruhend, vermerken, verschlossen, zuruecksetzen
highlights.py          check, new_state, observe, score, zustand
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kennzahlen.py          einwertig, prometheus, prozess, stand, veroeffentlichen, zeile
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
kickapi.py             app_token, broadcaster_id, channel_info, class PusherGeschlossen, configure, naechster_cluster, naechster_key, oauth_exchange, pusher_fehler, pusher_lage, pusher_pause, pusher_url, schliessgrund, search_category, send_message, slug, timeout_user, update_channel, user_token
kickzentrifugo.py      als_frame, antwort_fehler, class KickZentrifugoFehler, connect_cmd, fehler_code, ist_ping, kanal, lage, neue_client_id, neues_token, pause, refresh_cmd, subscribe_cmd, token_aus, ttl_aus, verbindung_body, ws_url_aus, zerlegen, zugang
kindprozess.py         alle_beenden, ausfuehren, beenden, lage, zuruecksetzen
kiwahl.py              backend, lokal_stand, lokal_zuerst, normal, provider
lagebild.py            bauen, restream_lage
lastvorsorge.py        freie_kerne, jung, startstufe
laufstand.py           befehl, veraltet, vergleich
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
linkvideo.py           abklingzeit_s, an, aufraeumen, ausgabe_lesen, befehl, bildunterschrift, configure, darf, grund, holen, ist_tiktok, links, max_dauer_s, sperre, werkzeug
livecache.py           aufraeumen, aufraeumen_faellig, dauer, einflug, frisch, holen, setzen, statistik, zaehle, zaehler_zuruecksetzen
livefolge.py           beste_url, braucht_url_nachschlag, hat_stream_url, last_dehnung, live_gesehen, offline_bestaetigt, poll_abstand, ruhezeit
livemeldung.py         live_an, live_aus
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             fuer_log, redact_cookie_zeilen, redact_pull_urls, redact_stream_urls, url_ohne_zugang
logschleuse.py         class Schleuse, einreihen, entkoppeln, nachziehen, schwaerzen, stoppen, synchrone_handler, verloren, wartend, zuruecksetzen
looplag.py             bremser, erfassen, lage, spaeher_starten, stelle_aus_rahmen, takt, zuruecksetzen
loyalty.py             award_chat, award_return, configure, enabled, leaderboard, rank_for, status
mariadbumzug.py        class UmzugAbgebrochen, env_setzen, geoeffnet_von, in_benutzung, quelle_zaehlen, umziehen, vergleichen, ziel_zaehlen
marketing.py           ai_flavor, class MarketingConfig, class MarketingState, compose, config, configure, default_targets, enabled, has_content, next_due_ts, post_discord, post_telegram, publish, should_post, state, state_save, variants
meldetakt.py           erfolg, gestoert, melden, zuruecksetzen, zusatz
memeklip.py            class Fenster, frage, lies_urteil, soll_clippen
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
modki.py               frage, lies_klassifikation, lies_schimpfwoerter
modstats.py            ist_moderation, plattform, quellen, verdichte, zaehlt
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
oauthredirect.py       configure, public_base_url, redirect_env, redirect_public, redirect_source, redirect_uri
outcomes.py            get_outcome_breakdown
overlaybrowser.py      browser_cmd, class Dauerbrowser, class OverlayBrowserFehler
overlaytext.py         configure, latest_popularity, ov_atomic_write, ov_bar, ov_oneline, overlay_src_ok
persona.py             —
piper_voices.py        available, bin_pfad, configure, data_dir, list_voices, resolve, resolve_model_path, roots, voice_dirs, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
profildetail.py        datum, felder, kennzahlen, kontotyp, verlauf
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
prueflage.py           fuer_healthz, lage, merken, runde_gelaufen, uebersicht, vergessen
qrsvg.py               qr_svg
quellprobe.py          empfehlung, form, kurz, main, maske, messen, probe_durchreicher, probe_ffprobe, probe_html, probe_ytdlp, ttl
quellstat.py           lage, zaehlen, zuruecksetzen
reccmd.py              build_recording_cmd, configure
recdb.py               configure, find_recordings_by_fingerprint, get_all_checks, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
resolvergrund.py       http_grund, quelle_lage, quelle_laut, text
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       betroffene_ziele, ein_start_je_ziel, fenstergroesse, freigeben, http_url, looks_like_source_expired, normalize_ingest, slot_belegt, startend, url_host
restreamcfg.py         active_platforms, aktiv, bereite_ziele, bruecke, bruecke_luecke, bruecke_offline, chat_src_ok, discord_invite, enabled, ingest, key_gesetzt, kick_channel_url, overlay, stall_timeout, verify, verify_karenz, verify_misses, verify_takt, yt_oauth_configured, ziel
restreamcmd.py         build, configure, drossel_avatar_aus, drossel_bitrate, drossel_canvas, drossel_fps, drossel_preset, drossel_zusatz, fueller, quell_eingang, schriftart, zubringer
restreamgesundheit.py  blind_markieren, frische_tee_fehler, marke_setzen
restreamstate.py       guard, haken, laufende, layout_mode, mgr
restrend.py            rising_trend
retention.py           scan
revenue.py             is_revenue_platform, normalisieren, sql_in
schema.py              anlegen, create_schema, index_sicher, kollation_angleichen, modultabellen, parameter, spalten_nachziehen
schemastand.py         lege_an, lies, pruefe, schreibe, streng
schnappschuss.py       class Schnappschuss
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendebruecke.py        class Bruecke, class TsUmschreiber, ist_keyframe, pat_pmt_pid, pes_zeit, pid, pmt_stroeme, pmt_urteil, video_pid, weiche_grund
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sicherpfad.py          pruefe_unter, sicher_join, sicherer_name, unter
sicherungspruefung.py  archiv_lesbar, dump_vollstaendig, pruefen
speicherpflege.py      abgelaufene_weg, alte_stempel_weg, groessen
spendeninfo.py         krypto, paypal, paypal_url, stand, text
spendenziel.py         eingang, fenster_start, ist_monatlich, stand, summe, zeitraum, ziel_eur
sqldialekt.py          bei_konflikt
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache
storage.py             class BestandUnbekannt, cleanup, forecast, notfall_raeumen, stats
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
suche.py               universal_search
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
systemprobe.py         active_recorder, ai_alive, ai_calls_total, cache_leeren, cached_probe, configure, cpu_load_snapshot, disk_pct, recorder_pref, recordings_dir, redis_alive, redis_url, redis_version
telegramfehler.py      dashboard_umzug, dauer_text, ersatz, grund, ist_fehler, ist_telegram_chat, nur_telegram, standardgruppe, text, zuruecksetzen
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
tgmarkdown.py          html_zu_md, teilen
tiktokcheck.py         account_exists, configure
tiktokheaders.py       configure
tonspur.py             class Fehlschlag, garantie, garantie_cmd, hat_ton, hat_tonspur, ist_tonlos_fehler, nachruest_cmd, pruef_cmd, pruefen, sichern, stille_eingabe
topicumzug.py          alte_themen, angekommen, erledigt, gesendet, lade, offen, schluessel, speichere
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
tunnelwacht.py         lage, meldung, probe, probe_cmd
twitchoauth.py         access_token, authorize_url, configure, create_clip, exchange_code, forget, login_name, search_category, status, timeout_user, update_channel
updater.py             ausfuehrbar_im_archiv, build_plan, check, class Plan, class UpdaterConfig, commit_zip_url, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, rechte_angleichen, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                datei_in
version.py             build_stamp, changelog, current, latest, summary_line
videoteil.py           configure, dauer, ist_kaputter_container, kopier_teilen, neu_kodieren, platz_reicht, reparieren, wegwerfen, zeitstempel_richten, zu_gross
webserver.py           bindung, ist_loopback, schema, threads, tls_lage, waehle
whispercfg.py          geladen, name, verfuegbar, waehle
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytdlpurl.py            nur_frische, urls_aus_json
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status, upload_clip
```

## brain/ — öffentliche Symbole

```
__init__.py            class Brain, get_brain
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DatabaseAgent, class DiskAgent, class GrafanaAgent, class HealthAgent, class LearningAgent, class PrometheusAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class SwapAgent, class ToxicityAgent, class UptimeAgent
knowledge.py           class KnowledgeGraph
llm.py                 class BudgetExhausted, class LLMRuntime
memory.py              class Memory
report.py              weekly
router.py              class Task, class TaskRouter, class Unhandled
rules.py               class Rule, class RulesEngine
scheduler.py           class Scheduler, frische_intervalle
semantic.py            class SemanticMemory
state.py               class Entity, class StateMachine
test_bughunt.py        db_conn, main
test_m1.py             main
test_m3.py             main
test_m4.py             main
test_m5.py             main
test_m6.py             class LlamaCppMock, main
test_m7.py             db_conn, main
```
